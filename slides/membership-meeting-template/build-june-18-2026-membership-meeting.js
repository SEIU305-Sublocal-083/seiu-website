"use strict";

const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");
const {
  autoFontSize,
  calcTextBox,
  imageSizingContain,
  imageSizingCrop,
  safeOuterShadow,
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers");

const ROOT = __dirname;
const OUT_DIR = path.join(ROOT, "output");
const PPTX_PATH = path.join(OUT_DIR, "membership-meeting-june-18-2026.pptx");
const logoPath = path.resolve(ROOT, "../../images/logo.png");
const rallyQrPath = path.resolve(ROOT, "../../images/rally-signup-qr.png");
const fistsPath = path.resolve(
  ROOT,
  "../../resources/zoom-backgrounds/2026-bargaining/SEIU-503-Bargaining-2026-Fists-Landscape.png"
);
const campusPath = path.resolve(
  ROOT,
  "../../resources/zoom-backgrounds/2026-bargaining/SEIU-503-Bargaining-2026-Campus-Landscape.png"
);

const theme = {
  purpleDark: "4C1D95",
  purple: "7C3AED",
  purpleMid: "6D28D9",
  purpleLight: "EDE9FE",
  purplePale: "F5F3FF",
  amber: "F59E0B",
  amberLight: "FEF3C7",
  greenDark: "14532D",
  greenLight: "DCFCE7",
  redDark: "7F1D1D",
  redLight: "FEE2E2",
  dark: "111827",
  light: "F9FAFB",
  white: "FFFFFF",
  text: "1F2937",
  textSecondary: "374151",
  muted: "6B7280",
  border: "D1D5DB",
  borderSoft: "E5E7EB",
  headFont: "Lora",
  bodyFont: "Inter",
};

const layout = {
  slideW: 13.333,
  slideH: 7.5,
  marginX: 0.72,
  contentW: 11.89,
  headerY: 0.38,
  headerRuleY: 0.78,
  titleY: 1.08,
  footerY: 7.08,
  cardRadius: 0.08,
  shadow: safeOuterShadow("000000", 0.08, 45, 1.2, 0.8),
};

fs.mkdirSync(OUT_DIR, { recursive: true });

function addBackground(slide, color = theme.light) {
  slide.background = { color };
}

function addHeader(slide, pageNum, section) {
  slide.addText("SEIU Local 503 at Oregon State University", {
    x: layout.marginX,
    y: layout.headerY,
    w: 5.8,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 9.2,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
  });
  slide.addText(section, {
    x: 8.25,
    y: layout.headerY,
    w: 3.2,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 8.8,
    color: theme.muted,
    align: "right",
    margin: 0,
  });
  slide.addText(String(pageNum).padStart(2, "0"), {
    x: 11.85,
    y: layout.headerY,
    w: 0.5,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 8.8,
    color: theme.muted,
    align: "right",
    margin: 0,
  });
  slide.addShape("line", {
    x: layout.marginX,
    y: layout.headerRuleY,
    w: layout.contentW,
    h: 0,
    line: { color: theme.borderSoft, pt: 1 },
  });
}

function addFooter(slide) {
  slide.addText("Membership meeting | June 18, 2026", {
    x: layout.marginX,
    y: layout.footerY,
    w: 3.7,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 9,
    color: theme.muted,
    margin: 0,
  });
  slide.addText("local083.org/rally", {
    x: 9.55,
    y: layout.footerY,
    w: 2.75,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 9.5,
    bold: true,
    color: theme.purpleDark,
    align: "right",
    margin: 0,
  });
}

function addCard(slide, x, y, w, h, opts = {}) {
  slide.addShape("roundRect", {
    x,
    y,
    w,
    h,
    rectRadius: opts.radius || layout.cardRadius,
    line: { color: opts.lineColor || theme.border, pt: opts.linePt || 1 },
    fill: { color: opts.fill || theme.white, transparency: opts.transparency || 0 },
    shadow: opts.shadow === false ? undefined : layout.shadow,
  });
}

function addTitle(slide, title, subtitle, opts = {}) {
  const titleBox = {
    x: layout.marginX,
    y: opts.y || layout.titleY,
    w: opts.w || 9.5,
    h: opts.h || 0.74,
  };
  slide.addText(title, {
    ...autoFontSize(title, theme.headFont, {
      ...titleBox,
      fontSize: opts.fontSize || 36,
      minFontSize: opts.minFontSize || 24,
      maxFontSize: opts.maxFontSize || 42,
      bold: true,
      color: opts.color || theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });
  if (!subtitle) return;
  const measured = calcTextBox(opts.subtitleSize || 18.5, {
    text: subtitle,
    w: opts.subtitleW || 9.7,
    fontFace: theme.bodyFont,
    margin: 0,
  });
  slide.addText(subtitle, {
    x: titleBox.x,
    y: titleBox.y + (opts.subtitleOffset || 0.92),
    w: opts.subtitleW || 9.7,
    h: Math.min(measured.h, opts.subtitleH || 0.72),
    fontFace: theme.bodyFont,
    fontSize: opts.subtitleSize || 18.5,
    color: opts.subtitleColor || theme.textSecondary,
    margin: 0,
    fit: "shrink",
  });
}

function addLabel(slide, text, x, y, w, opts = {}) {
  slide.addText(text, {
    x,
    y,
    w,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: opts.fontSize || 8.8,
    bold: true,
    color: opts.color || theme.purpleDark,
    margin: 0,
    charSpace: 0.2,
  });
}

function addPill(slide, text, x, y, w, opts = {}) {
  slide.addShape("roundRect", {
    x,
    y,
    w,
    h: opts.h || 0.48,
    rectRadius: 0.08,
    line: { color: opts.lineColor || theme.purpleLight, pt: 1 },
    fill: { color: opts.fill || theme.purpleLight },
  });
  slide.addText(text, {
    x: x + 0.12,
    y: y + 0.13,
    w: w - 0.24,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: opts.fontSize || 12,
    bold: true,
    color: opts.color || theme.purpleDark,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
}

function addBulletList(slide, items, box, opts = {}) {
  const fontSize = opts.fontSize || 18;
  const runs = items.map((item, index) => ({
    text: item,
    options: {
      bullet: { indent: opts.indent || 15 },
      breakLine: index < items.length - 1,
    },
  }));
  const measured = calcTextBox(fontSize, {
    text: runs,
    w: box.w,
    fontFace: theme.bodyFont,
    margin: 0,
    paraSpaceAfter: opts.paraSpaceAfter || 4,
  });
  slide.addText(runs, {
    x: box.x,
    y: box.y,
    w: box.w,
    h: box.h || Math.min(measured.h, opts.maxH || 3.2),
    fontFace: theme.bodyFont,
    fontSize,
    color: opts.color || theme.text,
    margin: 0,
    paraSpaceAfter: opts.paraSpaceAfter || 4,
    valign: "top",
    fit: "shrink",
  });
}

function addNumberedAction(slide, n, text, x, y, w, opts = {}) {
  slide.addShape("ellipse", {
    x,
    y: y + 0.03,
    w: 0.34,
    h: 0.34,
    line: { color: opts.fill || theme.purpleMid, transparency: 100 },
    fill: { color: opts.fill || theme.purpleMid },
  });
  slide.addText(String(n), {
    x,
    y: y + 0.12,
    w: 0.34,
    h: 0.12,
    fontFace: theme.bodyFont,
    fontSize: 9.8,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
  });
  slide.addText(text, {
    x: x + 0.52,
    y,
    w,
    h: 0.28,
    fontFace: theme.bodyFont,
    fontSize: opts.fontSize || 17.5,
    bold: true,
    color: opts.color || theme.text,
    margin: 0,
    fit: "shrink",
  });
}

function finalize(slide, pptx, opts = {}) {
  if (!opts.skipOverlapCheck) warnIfSlideHasOverlaps(slide, pptx, { muteContainment: true });
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

function titleSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide, theme.purpleDark);
  if (fs.existsSync(fistsPath)) {
    slide.addImage({ path: fistsPath, ...imageSizingCrop(fistsPath, 6.72, 0, 6.613, 7.5) });
    slide.addShape("rect", {
      x: 6.72,
      y: 0,
      w: 6.613,
      h: 7.5,
      line: { color: theme.purpleDark, transparency: 100 },
      fill: { color: theme.purpleDark, transparency: 38 },
    });
  }
  slide.addShape("rect", {
    x: 0,
    y: 0,
    w: 7.18,
    h: 7.5,
    line: { color: theme.purpleDark, transparency: 100 },
    fill: { color: theme.purpleDark },
  });
  if (fs.existsSync(logoPath)) {
    slide.addImage({ path: logoPath, ...imageSizingContain(logoPath, 0.78, 0.78, 0.78, 0.78) });
  }
  slide.addText("SEIU Local 083", {
    x: 1.72,
    y: 1.02,
    w: 2.5,
    h: 0.2,
    fontFace: theme.bodyFont,
    fontSize: 13,
    bold: true,
    color: theme.white,
    margin: 0,
  });
  slide.addText("June\nMembership\nMeeting", {
    x: 0.78,
    y: 1.62,
    w: 5.65,
    h: 2.18,
    fontFace: theme.headFont,
    fontSize: 42,
    bold: true,
    color: theme.white,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("Contract power starts with turnout.", {
    x: 0.82,
    y: 4.0,
    w: 5.3,
    h: 0.38,
    fontFace: theme.bodyFont,
    fontSize: 24,
    bold: true,
    color: "E9D5FF",
    margin: 0,
  });
  ["Thursday, June 18", "Noon to 1 p.m.", "Online via Zoom"].forEach((detail, i) => {
    addPill(slide, detail, 0.82 + i * 1.78, 4.76, 1.64, {
      fill: theme.white,
      lineColor: theme.white,
      color: theme.purpleDark,
      fontSize: 11,
      h: 0.52,
    });
  });
  slide.addText("We are using this meeting to turn bargaining updates into action before the June 30 rally.", {
    x: 0.82,
    y: 5.76,
    w: 5.1,
    h: 0.68,
    fontFace: theme.bodyFont,
    fontSize: 17.8,
    color: theme.white,
    margin: 0,
    fit: "shrink",
  });
  finalize(slide, pptx, { skipOverlapCheck: true });
}

function agendaSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 2, "Agenda");
  addTitle(slide, "Today is about June 30", "Each update connects to one question: what can members do before the rally?", { subtitleSize: 18 });
  const agenda = [
    ["12:00", "Welcome and the turnout ask"],
    ["12:05", "Bargaining update"],
    ["12:20", "Layoff rights and job security"],
    ["12:35", "New Local 083 office"],
    ["12:40", "Oregon House and Senate outreach"],
    ["12:50", "June 29 sign-making party"],
    ["12:55", "Commitments before we leave"],
  ];
  agenda.forEach(([time, item], index) => {
    const y = 2.82 + index * 0.5;
    addCard(slide, 0.9, y, 9.2, 0.48, {
      fill: index === 0 || index === agenda.length - 1 ? theme.purplePale : theme.white,
      lineColor: theme.borderSoft,
      shadow: false,
    });
    slide.addText(time, {
      x: 1.15,
      y: y + 0.13,
      w: 0.78,
      h: 0.12,
      fontFace: theme.bodyFont,
      fontSize: 11,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
    });
    slide.addText(item, {
      x: 2.1,
      y: y + 0.09,
      w: 7.15,
      h: 0.2,
      fontFace: theme.bodyFont,
      fontSize: 17.2,
      bold: index === 0 || index === agenda.length - 1,
      color: theme.text,
      margin: 0,
      fit: "shrink",
    });
  });
  addCard(slide, 10.58, 2.82, 1.52, 3.35, { fill: theme.purpleDark, lineColor: theme.purpleDark, shadow: false });
  slide.addText("No passive updates.", {
    x: 10.83,
    y: 3.4,
    w: 1.02,
    h: 0.82,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  slide.addText("Every section ends with action.", {
    x: 10.83,
    y: 4.52,
    w: 1.02,
    h: 0.82,
    fontFace: theme.bodyFont,
    fontSize: 13,
    bold: true,
    color: "E9D5FF",
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide);
  finalize(slide, pptx);
}

function rallyFrameSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 3, "June 30 frame");
  addTitle(slide, "Why turnout matters", "A strong rally tells management that members are paying attention and ready to act.", { subtitleSize: 18 });
  const cards = [
    ["Bargaining", "Management needs to see that proposals have consequences with members."],
    ["Job security", "Layoff protections matter most when members are organized to enforce them."],
    ["Public pressure", "Lawmakers need to hear why OSU workers and our contract matter."],
  ];
  cards.forEach(([title, body], index) => {
    const x = 0.9 + index * 3.66;
    addCard(slide, x, 3.02, 3.22, 2.18, { fill: index === 0 ? theme.purplePale : theme.white, lineColor: theme.borderSoft, shadow: false });
    slide.addText(title, {
      x: x + 0.28,
      y: 3.32,
      w: 2.55,
      h: 0.22,
      fontFace: theme.headFont,
      fontSize: 22,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
    });
    slide.addText(body, {
      x: x + 0.28,
      y: 3.88,
      w: 2.58,
      h: 0.72,
      fontFace: theme.bodyFont,
      fontSize: 15.3,
      color: theme.textSecondary,
      margin: 0,
      fit: "shrink",
    });
  });
  addCard(slide, 0.9, 5.76, 10.9, 0.64, { fill: theme.purpleDark, lineColor: theme.purpleDark, shadow: false });
  slide.addText("The rally is not extra. It is part of how we bargain.", {
    x: 1.25,
    y: 5.96,
    w: 10.15,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 18,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
  });
  addFooter(slide);
  finalize(slide, pptx);
}

function bargainingSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 4, "Bargaining update");
  addTitle(slide, "What members need to know", "Keep this plain: what is on the table, what is at stake, and why member turnout changes the room.", { subtitleSize: 17.3 });
  addCard(slide, 0.9, 2.78, 5.08, 3.18, { fill: theme.redLight, lineColor: "FECACA", shadow: false });
  slide.addText("Management is offering", {
    x: 1.22,
    y: 3.05,
    w: 4.2,
    h: 0.24,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.redDark,
    margin: 0,
  });
  addBulletList(
    slide,
    [
      "No raises or COLA for four years",
      "Pressure on overtime and leave rights",
      "Weaker standards when members need stronger protections",
    ],
    { x: 1.25, y: 3.55, w: 4.24, h: 1.7 },
    { fontSize: 16.2, paraSpaceAfter: 3 }
  );
  addCard(slide, 6.34, 2.78, 5.48, 3.18, { fill: theme.greenLight, lineColor: "BBF7D0", shadow: false });
  slide.addText("Our union is fighting for", {
    x: 6.68,
    y: 3.05,
    w: 4.4,
    h: 0.24,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.greenDark,
    margin: 0,
  });
  addBulletList(
    slide,
    [
      "Real raises and a fair contract",
      "Stronger layoff and workplace protections",
      "A contract that respects the work classified staff do",
    ],
    { x: 6.72, y: 3.55, w: 4.58, h: 1.7 },
    { fontSize: 16.2, paraSpaceAfter: 3 }
  );
  addPill(slide, "Turnout makes the stakes visible.", 4.3, 6.35, 4.3, { fill: theme.purpleDark, lineColor: theme.purpleDark, color: theme.white, h: 0.5, fontSize: 14 });
  addFooter(slide);
  finalize(slide, pptx);
}

function layoffRightsSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 5, "Layoff rights");
  addTitle(slide, "Layoff rights are contract rights", "Members should not face rumors, notices, or displacement questions alone.", { subtitleSize: 18 });
  addCard(slide, 0.9, 2.68, 4.82, 3.3, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  addLabel(slide, "IF YOU HEAR A RUMOR OR RECEIVE NOTICE", 1.25, 2.98, 3.6, { fontSize: 9.5 });
  addNumberedAction(slide, 1, "Contact our union.", 1.25, 3.42, 3.5);
  addNumberedAction(slide, 2, "Talk with a steward.", 1.25, 4.02, 3.5);
  addNumberedAction(slide, 3, "Keep records and dates.", 1.25, 4.62, 3.5);
  addNumberedAction(slide, 4, "Do not navigate it alone.", 1.25, 5.22, 3.5);
  addCard(slide, 6.26, 2.68, 5.56, 3.3, { fill: theme.purplePale, lineColor: theme.purpleLight, shadow: false });
  slide.addText("Why this belongs in the rally frame", {
    x: 6.62,
    y: 3.05,
    w: 4.62,
    h: 0.26,
    fontFace: theme.headFont,
    fontSize: 24,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
  });
  slide.addText("Layoff language, timelines, bumping rights, and enforcement matter because job security is not automatic. Members protect it by knowing our rights and showing up together.", {
    x: 6.62,
    y: 3.72,
    w: 4.58,
    h: 1.26,
    fontFace: theme.bodyFont,
    fontSize: 18,
    bold: true,
    color: theme.text,
    margin: 0,
    fit: "shrink",
  });
  addPill(slide, "083stewards@seiu503.org", 7.05, 5.34, 3.58, { fill: theme.white, lineColor: theme.white, fontSize: 13, h: 0.5 });
  addFooter(slide);
  finalize(slide, pptx);
}

function officeSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 6, "Local 083 office");
  addTitle(slide, "We have a new office", "This is organizing capacity: a place for questions, planning, outreach, and member follow-up.", { subtitleSize: 18 });
  addCard(slide, 0.9, 2.8, 10.9, 2.95, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  const uses = [
    ["Meet", "Members can talk through questions and next steps."],
    ["Plan", "We can prep outreach, materials, and rally turnout."],
    ["Follow up", "We can connect members with stewards and leaders."],
  ];
  uses.forEach(([title, body], index) => {
    const x = 1.35 + index * 3.35;
    addCard(slide, x, 3.28, 2.65, 1.36, { fill: index === 1 ? theme.purplePale : theme.light, lineColor: theme.borderSoft, shadow: false });
    slide.addText(title, {
      x: x + 0.23,
      y: 3.52,
      w: 2.1,
      h: 0.22,
      fontFace: theme.headFont,
      fontSize: 22,
      bold: true,
      color: theme.purpleDark,
      align: "center",
      margin: 0,
    });
    slide.addText(body, {
      x: x + 0.23,
      y: 3.9,
      w: 2.1,
      h: 0.4,
      fontFace: theme.bodyFont,
      fontSize: 13.2,
      color: theme.textSecondary,
      align: "center",
      margin: 0,
      fit: "shrink",
    });
  });
  addPill(slide, "Use the office to build the June 30 turnout plan.", 3.36, 5.18, 5.95, { fill: theme.purpleDark, lineColor: theme.purpleDark, color: theme.white, fontSize: 13.5, h: 0.5 });
  addFooter(slide);
  finalize(slide, pptx);
}

function legislativeSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 7, "Legislative outreach");
  addTitle(slide, "Members need to talk with lawmakers", "We are looking for members to meet with Oregon House and Senate members before the rally.", { subtitleSize: 18 });
  addCard(slide, 0.9, 2.72, 5.2, 3.28, { fill: theme.purplePale, lineColor: theme.purpleLight, shadow: false });
  slide.addText("You do not need to be a policy expert.", {
    x: 1.25,
    y: 3.1,
    w: 4.42,
    h: 0.62,
    fontFace: theme.headFont,
    fontSize: 28,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("You need to be able to explain what your job is, what OSU workers are facing, and why this contract matters.", {
    x: 1.25,
    y: 4.18,
    w: 4.3,
    h: 0.86,
    fontFace: theme.bodyFont,
    fontSize: 18,
    color: theme.text,
    margin: 0,
    fit: "shrink",
  });
  addCard(slide, 6.62, 2.72, 5.2, 3.28, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  addLabel(slide, "STORIES LAWMAKERS NEED TO HEAR", 6.98, 3.05, 3.9, { fontSize: 9.5 });
  addBulletList(
    slide,
    ["Wages and cost of living", "Staffing and workload", "Layoffs and job security", "How classified staff keep OSU running"],
    { x: 7.0, y: 3.55, w: 4.05, h: 1.95 },
    { fontSize: 16.8, paraSpaceAfter: 2 }
  );
  addFooter(slide);
  finalize(slide, pptx);
}

function signMakingSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide, theme.purpleDark);
  if (fs.existsSync(campusPath)) {
    slide.addImage({ path: campusPath, ...imageSizingCrop(campusPath, 0, 0, 13.333, 7.5) });
    slide.addShape("rect", {
      x: 0,
      y: 0,
      w: 13.333,
      h: 7.5,
      line: { color: theme.purpleDark, transparency: 100 },
      fill: { color: theme.purpleDark, transparency: 34 },
    });
  }
  slide.addText("Sign-making party", {
    x: 0.86,
    y: 1.05,
    w: 6.6,
    h: 0.76,
    fontFace: theme.headFont,
    fontSize: 44,
    bold: true,
    color: theme.white,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("Monday, June 29 | 5-7 p.m.\nWestminster House on Monroe", {
    x: 0.9,
    y: 2.22,
    w: 5.95,
    h: 0.86,
    fontFace: theme.bodyFont,
    fontSize: 23,
    bold: true,
    color: "E9D5FF",
    margin: 0,
    fit: "shrink",
  });
  addCard(slide, 0.9, 3.68, 5.72, 1.58, { fill: theme.white, lineColor: theme.white, shadow: false });
  slide.addText("Come make signs, bring a coworker, and help us get ready to show OSU that classified staff are organized for a fair contract.", {
    x: 1.22,
    y: 4.02,
    w: 5.05,
    h: 0.62,
    fontFace: theme.bodyFont,
    fontSize: 18,
    bold: true,
    color: theme.text,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("The night before is part of the turnout plan.", {
    x: 0.92,
    y: 6.0,
    w: 6.0,
    h: 0.26,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.white,
    margin: 0,
  });
  finalize(slide, pptx, { skipOverlapCheck: true });
}

function rallyCtaSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide, theme.purpleDark);
  if (fs.existsSync(fistsPath)) {
    slide.addImage({ path: fistsPath, ...imageSizingCrop(fistsPath, 0, 0, 13.333, 7.5) });
    slide.addShape("rect", {
      x: 0,
      y: 0,
      w: 13.333,
      h: 7.5,
      line: { color: theme.purpleDark, transparency: 100 },
      fill: { color: theme.purpleDark, transparency: 44 },
    });
  }
  slide.addText("June 30: show up for our contract", {
    x: 0.82,
    y: 0.92,
    w: 8.0,
    h: 0.95,
    fontFace: theme.headFont,
    fontSize: 42,
    bold: true,
    color: theme.white,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("Tuesday, June 30 | Noon-1 p.m. | McNary Field", {
    x: 0.86,
    y: 2.14,
    w: 7.0,
    h: 0.28,
    fontFace: theme.bodyFont,
    fontSize: 21,
    bold: true,
    color: "E9D5FF",
    margin: 0,
  });
  addCard(slide, 0.9, 3.08, 5.7, 2.12, { fill: theme.white, lineColor: theme.white, shadow: false });
  addBulletList(
    slide,
    ["Sign up now", "Wear purple", "Bring one coworker", "Help turn out your work area"],
    { x: 1.24, y: 3.42, w: 4.88, h: 1.28 },
    { fontSize: 18.2, paraSpaceAfter: 2, color: theme.text }
  );
  addCard(slide, 8.08, 2.68, 3.62, 3.75, { fill: theme.white, lineColor: theme.white, shadow: false });
  if (fs.existsSync(rallyQrPath)) {
    slide.addImage({ path: rallyQrPath, ...imageSizingContain(rallyQrPath, 8.52, 3.0, 2.75, 2.75) });
  }
  slide.addText("local083.org/rally", {
    x: 8.38,
    y: 5.88,
    w: 3.08,
    h: 0.24,
    fontFace: theme.bodyFont,
    fontSize: 19,
    bold: true,
    color: theme.purpleDark,
    align: "center",
    margin: 0,
  });
  finalize(slide, pptx, { skipOverlapCheck: true });
}

function commitmentsSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 10, "Commitments");
  addTitle(slide, "Before you log off", "Pick the next step you can take before June 30.", { subtitleSize: 18 });
  const actions = [
    "Sign up for the June 30 rally.",
    "Bring one coworker with you.",
    "Come to the June 29 sign-making party.",
    "Volunteer for a legislative meeting.",
    "Talk to a steward if you have layoff questions.",
    "Help turn out your work area.",
  ];
  actions.forEach((action, index) => {
    const y = 2.86 + index * 0.52;
    addNumberedAction(slide, index + 1, action, 1.08, y, 6.6, { fontSize: 17.2 });
  });
  addCard(slide, 8.25, 2.7, 3.55, 2.15, { fill: theme.purplePale, lineColor: theme.purpleLight, shadow: false });
  slide.addText("Contact paths", {
    x: 8.6,
    y: 3.05,
    w: 2.7,
    h: 0.24,
    fontFace: theme.headFont,
    fontSize: 24,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
  });
  slide.addText("083execteam@seiu503.org\n083stewards@seiu503.org", {
    x: 8.6,
    y: 3.62,
    w: 2.82,
    h: 0.52,
    fontFace: theme.bodyFont,
    fontSize: 14.6,
    bold: true,
    color: theme.text,
    margin: 0,
    fit: "shrink",
  });
  addCard(slide, 0.9, 6.25, 10.9, 0.54, { fill: theme.purpleDark, lineColor: theme.purpleDark, shadow: false });
  slide.addText("Our contract is stronger when members show up together.", {
    x: 1.22,
    y: 6.42,
    w: 10.2,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 16.5,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
  });
  addFooter(slide);
  finalize(slide, pptx);
}

async function main() {
  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "SEIU Local 503 Sublocal 083";
  pptx.subject = "Membership meeting deck for June 18, 2026";
  pptx.title = "Membership Meeting June 18 2026";
  pptx.company = "SEIU Local 503 at Oregon State University";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: theme.headFont,
    bodyFontFace: theme.bodyFont,
    lang: "en-US",
  };

  titleSlide(pptx);
  agendaSlide(pptx);
  rallyFrameSlide(pptx);
  bargainingSlide(pptx);
  layoffRightsSlide(pptx);
  officeSlide(pptx);
  legislativeSlide(pptx);
  signMakingSlide(pptx);
  rallyCtaSlide(pptx);
  commitmentsSlide(pptx);

  await pptx.writeFile({ fileName: PPTX_PATH });
  console.log(PPTX_PATH);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
