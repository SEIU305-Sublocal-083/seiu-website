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
const PPTX_PATH = path.join(OUT_DIR, "membership-meeting-may-21-2026.pptx");
const logoPath = path.resolve(ROOT, "../../images/logo.png");
const fistsPath = path.resolve(
  ROOT,
  "../../resources/zoom-backgrounds/2026-bargaining/SEIU-503-Bargaining-2026-Fists-Landscape.png"
);
const campusPath = path.resolve(
  ROOT,
  "../../resources/zoom-backgrounds/2026-bargaining/SEIU-503-Bargaining-2026-Campus-Landscape.png"
);
const headshotPath = path.resolve(
  ROOT,
  "../../images/5aae970a-ef7b-4ce3-9510-b28435672bf7-jax-headshot.webp"
);
const rallyQrPath = path.resolve(ROOT, "../../images/rally-signup-qr.png");

const theme = {
  purpleDark: "4C1D95",
  purple: "7C3AED",
  purpleMid: "6D28D9",
  purpleLight: "EDE9FE",
  purplePale: "F5F3FF",
  amber: "F59E0B",
  amberLight: "FEF3C7",
  redDark: "7F1D1D",
  redLight: "FEE2E2",
  greenDark: "14532D",
  greenLight: "DCFCE7",
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
  titleY: 1.1,
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
    x: 8.3,
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
  slide.addText("Membership meeting | May 21, 2026", {
    x: layout.marginX,
    y: layout.footerY,
    w: 3.4,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 9,
    color: theme.muted,
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
  const titleBox = { x: layout.marginX, y: opts.y || layout.titleY, w: opts.w || 9.2, h: opts.h || 0.72 };
  slide.addText(title, {
    ...autoFontSize(title, theme.headFont, {
      ...titleBox,
      fontSize: opts.fontSize || 36,
      minFontSize: opts.minFontSize || 24,
      maxFontSize: opts.maxFontSize || 40,
      bold: true,
      color: opts.color || theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });
  if (subtitle) {
    const measured = calcTextBox(opts.subtitleSize || 18.5, {
      text: subtitle,
      w: opts.subtitleW || 9.2,
      fontFace: theme.bodyFont,
      margin: 0,
    });
    slide.addText(subtitle, {
      x: titleBox.x,
      y: titleBox.y + 0.92,
      w: opts.subtitleW || 9.2,
      h: Math.min(measured.h, opts.subtitleH || 0.72),
      fontFace: theme.bodyFont,
      fontSize: opts.subtitleSize || 18.5,
      color: opts.subtitleColor || theme.textSecondary,
      margin: 0,
      fit: "shrink",
    });
  }
}

function addBulletList(slide, items, box, opts = {}) {
  const fontSize = opts.fontSize || 19;
  const runs = items.map((item, index) => ({
    text: item,
    options: { bullet: { indent: opts.indent || 16 }, breakLine: index < items.length - 1 },
  }));
  const measured = calcTextBox(fontSize, {
    text: runs,
    w: box.w,
    fontFace: theme.bodyFont,
    margin: 0,
    paraSpaceAfter: opts.paraSpaceAfter || 5,
  });
  slide.addText(runs, {
    x: box.x,
    y: box.y,
    w: box.w,
    h: opts.h || measured.h,
    fontFace: theme.bodyFont,
    fontSize,
    color: opts.color || theme.text,
    margin: 0,
    paraSpaceAfter: opts.paraSpaceAfter || 5,
    valign: "top",
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
    h: opts.h || 0.5,
    rectRadius: 0.08,
    line: { color: opts.lineColor || theme.purpleLight, pt: 1 },
    fill: { color: opts.fill || theme.purpleLight },
  });
  slide.addText(text, {
    x: x + 0.12,
    y: y + 0.14,
    w: w - 0.24,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: opts.fontSize || 12,
    bold: true,
    color: opts.color || theme.purpleDark,
    align: "center",
    margin: 0,
  });
}

function addSpeakerSpace(slide, x, y, w, h, label = "Speaker notes and member questions") {
  addCard(slide, x, y, w, h, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  slide.addShape("line", { x: x + 0.35, y: y + h - 0.58, w: w - 0.7, h: 0, line: { color: theme.borderSoft, pt: 1 } });
  slide.addText(label, {
    x: x + 0.35,
    y: y + h - 0.38,
    w: w - 0.7,
    h: 0.13,
    fontFace: theme.bodyFont,
    fontSize: 11,
    color: theme.muted,
    margin: 0,
  });
}

function finalize(slide, pptx, opts = {}) {
  if (!opts.skipOverlapCheck) warnIfSlideHasOverlaps(slide, pptx, { muteContainment: true });
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

function titleSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide, theme.purpleDark);
  if (fs.existsSync(campusPath)) {
    slide.addImage({ path: campusPath, ...imageSizingCrop(campusPath, 6.6, 0, 6.733, 7.5) });
    slide.addShape("rect", { x: 6.6, y: 0, w: 6.733, h: 7.5, line: { color: theme.purpleDark, transparency: 100 }, fill: { color: theme.purpleDark, transparency: 38 } });
  }
  slide.addShape("rect", { x: 0, y: 0, w: 7.2, h: 7.5, line: { color: theme.purpleDark, transparency: 100 }, fill: { color: theme.purpleDark } });
  slide.addImage({ path: logoPath, ...imageSizingContain(logoPath, 0.78, 0.78, 0.78, 0.78) });
  slide.addText("SEIU Local 083", {
    x: 1.74,
    y: 1.02,
    w: 2.5,
    h: 0.2,
    fontFace: theme.bodyFont,
    fontSize: 13,
    bold: true,
    color: theme.white,
    margin: 0,
  });
  slide.addText("Membership\nMeeting", {
    x: 0.78,
    y: 1.82,
    w: 5.7,
    h: 1.58,
    fontFace: theme.headFont,
    fontSize: 44,
    bold: true,
    color: theme.white,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("Bargaining update, member action, and what we do next.", {
    x: 0.82,
    y: 3.55,
    w: 5.1,
    h: 0.62,
    fontFace: theme.bodyFont,
    fontSize: 24,
    color: "E9D5FF",
    margin: 0,
  });
  const details = ["Thursday, May 21, 2026", "Noon to 1 p.m.", "MU 211 or Zoom"];
  details.forEach((detail, i) => {
    addPill(slide, detail, 0.82 + i * 1.9, 4.62, 1.76, { fill: theme.white, lineColor: theme.white, color: theme.purpleDark, fontSize: 12, h: 0.52 });
  });
  slide.addText("Our union is member-run. This meeting is where we hear what is happening, make the stakes plain, and leave with the next action.", {
    x: 0.82,
    y: 5.65,
    w: 5.1,
    h: 0.8,
    fontFace: theme.bodyFont,
    fontSize: 18,
    color: theme.white,
    margin: 0,
  });
  finalize(slide, pptx, { skipOverlapCheck: true });
}

function agendaSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 2, "Agenda");
  addTitle(slide, "Today's agenda", "Bargaining facts, member voices, and clear next steps.", { subtitleSize: 18 });
  const agenda = [
    "Welcome and introductions",
    "Bargaining update",
    "Membership update",
    "What management's offer means for us",
    "Workday transition CTA",
    "Rally for our Future",
    "Questions and next steps",
  ];
  agenda.forEach((item, index) => {
    const y = 2.88 + index * 0.56;
    addCard(slide, 0.9, y, 8.85, 0.56, { fill: index < 2 ? theme.purplePale : theme.white, lineColor: theme.borderSoft, shadow: false });
    slide.addText(String(index + 1).padStart(2, "0"), {
      x: 1.15,
      y: y + 0.16,
      w: 0.42,
      h: 0.1,
      fontFace: theme.bodyFont,
      fontSize: 12,
      bold: true,
      color: theme.purpleDark,
      align: "center",
      margin: 0,
    });
    slide.addText(item, {
      x: 1.78,
      y: y + 0.11,
      w: 6.8,
      h: 0.22,
      fontFace: theme.bodyFont,
      fontSize: 18.5,
      bold: index < 2,
      color: theme.text,
      margin: 0,
    });
  });
  addCard(slide, 10.15, 2.88, 2.0, 3.05, { fill: theme.purpleDark, lineColor: theme.purpleDark, shadow: false });
  slide.addText("Leave with one action you can take and one coworker you can bring in.", {
    x: 10.28,
    y: 3.38,
    w: 1.48,
    h: 1.75,
    fontFace: theme.headFont,
    fontSize: 24,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide);
  finalize(slide, pptx);
}

function introductionSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 3, "Introductions");
  addTitle(slide, "Welcome and introductions", "Our union is led by members who represent our shared interests.", { subtitleSize: 18 });
  if (fs.existsSync(headshotPath)) {
    slide.addImage({ path: headshotPath, ...imageSizingCrop(headshotPath, 0.9, 2.62, 1.55, 1.55) });
  }
  addCard(slide, 2.75, 2.55, 3.9, 1.95, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  addLabel(slide, "PRESIDENT AND COMMUNICATIONS CHAIR", 3.05, 2.66, 3.1, { fontSize: 10 });
  slide.addText("Jax SN Johnson", {
    x: 3.05,
    y: 2.9,
    w: 3.0,
    h: 0.25,
    fontFace: theme.headFont,
    fontSize: 26,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
  });
  slide.addText("Opening the meeting and grounding us in the work ahead.", {
    x: 3.05,
    y: 3.3,
    w: 3.1,
    h: 0.32,
    fontFace: theme.bodyFont,
    fontSize: 16,
    color: theme.textSecondary,
    margin: 0,
  });
  addCard(slide, 7.0, 2.55, 4.7, 2.45, { fill: theme.purplePale, lineColor: theme.purpleLight, shadow: false });
  slide.addText("Updated Sublocal 083 leadership team", {
    x: 7.34,
    y: 2.90,
    w: 3.7,
    h: 0.24,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
  });
  addBulletList(
    slide,
    [
      "James Pavis, vice president",
      "Richard Keuneke, chief steward",
      "Jacob Harold, membership coordinator",
      "Gabriel Labarca, secretary",
      "Vinay Ramakrishnan, treasurer",
    ],
    { x: 7.45, y: 3.3, w: 3.9 },
    { fontSize: 13.8, paraSpaceAfter: 2 }
  );
  addCard(slide, 0.9, 5.32, 10.8, 0.9, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  slide.addText("Member-run means members shape the priorities, show up for each other, and make the contract campaign visible across campus.", {
    x: 1.18,
    y: 5.55,
    w: 10.1,
    h: 0.28,
    fontFace: theme.bodyFont,
    fontSize: 17.5,
    bold: true,
    color: theme.text,
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide);
  finalize(slide, pptx, { skipOverlapCheck: true });
}

function bargainingContextSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 4, "Bargaining");
  addTitle(slide, "Bargaining update", "Management has put takeaways on the table. Our union is fighting for standards members can live with.", { subtitleSize: 18 });
  if (fs.existsSync(fistsPath)) {
    slide.addImage({ path: fistsPath, ...imageSizingCrop(fistsPath, 8.25, 3.0, 3.7, 1.9) });
  }
  const priorities = [
    ["Fair wages", "Real raises, longevity, and pay that keeps up with costs."],
    ["Benefits", "Protect health coverage and pay schedule options."],
    ["Union power", "Orientations, steward access, and enforceable rights."],
    ["Employee protections", "AI, monitoring, leave, safety gear, weather, and immigration protections."],
  ];
  priorities.forEach(([title, body], index) => {
    const x = 0.9 + (index % 2) * 3.55;
    const y = 3.02 + Math.floor(index / 2) * 1.18;
    addCard(slide, x, y, 3.25, 1.16, { fill: index === 0 ? theme.purplePale : theme.white, lineColor: theme.borderSoft, shadow: false });
    slide.addText(title, {
      x: x + 0.26,
      y: y + 0.18,
      w: 2.6,
      h: 0.18,
      fontFace: theme.headFont,
      fontSize: 19,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
    });
    slide.addText(body, {
      x: x + 0.26,
      y: y + 0.5,
      w: 2.6,
      h: 0.25,
      fontFace: theme.bodyFont,
      fontSize: 13.5,
      color: theme.textSecondary,
      margin: 0,
    });
  });
  addCard(slide, 8.15, 5.15, 3.8, 1.35, { fill: theme.amberLight, lineColor: "FCD34D", shadow: false });
  slide.addText("The issue is not just one proposal. It is whether management can make our contract weaker while members absorb the cost.", {
    x: 8.48,
    y: 5.48,
    w: 3.12,
    h: 0.62,
    fontFace: theme.bodyFont,
    fontSize: 15.5,
    bold: true,
    color: theme.text,
    align: "center",
    margin: 0,
  });
  addFooter(slide);
  finalize(slide, pptx);
}

function sideBySideSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 5, "Bargaining side-by-side");
  addTitle(slide, "The offer on the table", "Use this side-by-side to talk with coworkers about what is at stake.", { subtitleSize: 18, subtitleH: 0.58 });
  addCard(slide, 0.9, 2.6, 5.35, 3.8, { fill: theme.redLight, lineColor: "FECACA", shadow: false });
  addCard(slide, 6.55, 2.6, 5.35, 3.8, { fill: theme.greenLight, lineColor: "BBF7D0", shadow: false });
  slide.addText("Management proposals", {
    x: 1.25,
    y: 2.9,
    w: 4.3,
    h: 0.25,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.redDark,
    margin: 0,
  });
  slide.addText("Our union proposals", {
    x: 6.9,
    y: 2.9,
    w: 4.3,
    h: 0.25,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.greenDark,
    margin: 0,
  });
  addBulletList(
    slide,
    [
      "No wage proposal until May 14",
      "Change overtime and reduce earnings",
      "Doctor's note after 3 sick days",
      "Limit bereavement leave",
      "Complicate vacation cash-out",
    ],
    { x: 1.25, y: 3.45, w: 4.55, h: 2.45 },
    { fontSize: 16.2, paraSpaceAfter: 3 }
  );
  addBulletList(
    slide,
    [
      "2026: CPI + 3%, at least 4%",
      "2027: CPI + 2%, at least 4%",
      "Longevity premium",
      "32-hour workweek pilot",
      "AI, monitoring, and benefits protections",
    ],
    { x: 6.9, y: 3.45, w: 4.55, h: 2.45 },
    { fontSize: 16.2, paraSpaceAfter: 3 }
  );
  addFooter(slide);
  finalize(slide, pptx);
}

function bargainingDelegateSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 6, "Bargaining delegate");
  addTitle(slide, "Bargaining delegate report", "Space for the bargaining delegate to explain what members need to know now.", { subtitleSize: 18 });
  ["What changed", "What management is offering", "What members need to understand"].forEach((prompt, index) => {
    addPill(slide, prompt, 0.9 + index * 3.12, 3.02, 2.82, { fill: theme.purplePale, lineColor: theme.purpleLight, fontSize: 14, h: 0.56 });
  });
  addSpeakerSpace(slide, 0.9, 3.85, 10.95, 2.45, "Open space for live remarks");
  addFooter(slide);
  finalize(slide, pptx);
}

function membershipSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 7, "Membership");
  addTitle(slide, "Membership builds bargaining power", "Rodger White: space to talk about signing members and moving coworkers to action.", { subtitleSize: 18 });
  const prompts = [
    ["Who signs", "Every coworker who wants a voice and vote in our union."],
    ["Why it matters", "Members ratify contracts, elect leaders, and shape our priorities."],
    ["What coworkers do next", "Join, ask questions, and bring one coworker into the meeting or rally."],
  ];
  prompts.forEach(([title, body], index) => {
    addCard(slide, 0.9 + index * 3.65, 3.02, 3.25, 1.28, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
    slide.addText(title, {
      x: 1.16 + index * 3.65,
      y: 3.19,
      w: 2.6,
      h: 0.18,
      fontFace: theme.headFont,
      fontSize: 20,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
    });
    slide.addText(body, {
      x: 1.16 + index * 3.65,
      y: 3.52,
      w: 2.7,
      h: 0.42,
      fontFace: theme.bodyFont,
      fontSize: 14.2,
      color: theme.textSecondary,
      margin: 0,
    });
  });
  addCard(slide, 0.9, 4.72, 10.95, 1.25, { fill: theme.purpleDark, lineColor: theme.purpleDark, shadow: false });
  slide.addText("Become a full member to have a voice and a vote.", {
    x: 1.35,
    y: 5.04,
    w: 10.0,
    h: 0.35,
    fontFace: theme.headFont,
    fontSize: 32,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide);
  finalize(slide, pptx);
}

function jamesPavisSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 8, "Member impact");
  addTitle(slide, "What these offers would do to us", "Vice President James Pavis: space to connect the offer to daily work, pay, leave, and enforceable rights.", { subtitleSize: 18 });
  const impacts = [
    ["Pay", "Lower overtime and no real raises mean members carry the cost."],
    ["Leave", "Shorter sick-note timelines and bereavement caps add pressure when members are already stretched."],
    ["Workplace power", "Every weaker article makes it harder to enforce the contract later."],
  ];
  impacts.forEach(([title, body], index) => {
    const y = 2.75 + index * 0.9;
    addCard(slide, 0.92, y, 4.65, 0.78, { fill: theme.purplePale, lineColor: theme.purpleLight, shadow: false });
    slide.addText(title, {
      x: 1.18,
      y: y + 0.18,
      w: 1.25,
      h: 0.16,
      fontFace: theme.headFont,
      fontSize: 18,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
    });
    slide.addText(body, {
      x: 2.55,
      y: y + 0.16,
      w: 2.7,
      h: 0.28,
      fontFace: theme.bodyFont,
      fontSize: 13.5,
      color: theme.textSecondary,
      margin: 0,
      fit: "shrink",
    });
  });
  addSpeakerSpace(slide, 6.15, 2.75, 5.7, 3.35, "Open space for James Pavis remarks");
  addFooter(slide);
  finalize(slide, pptx);
}

function workdaySlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 9, "Workday transition");
  addTitle(slide, "Save your records before Workday", "Protect your paycheck and time off banks before the transition creates problems.", { subtitleSize: 18 });
  addCard(slide, 0.9, 2.92, 10.95, 0.98, { fill: theme.amberLight, lineColor: "FCD34D", shadow: false });
  slide.addText("Save screenshots of your paycheck, time records, and vacation, sick, comp, and personal leave banks before the Workday transition.", {
    x: 1.25,
    y: 3.12,
    w: 10.2,
    h: 0.42,
    fontFace: theme.bodyFont,
    fontSize: 18,
    bold: true,
    color: theme.text,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  addBulletList(
    slide,
    [
      "Paycheck and pay stubs",
      "Time entries and approval status",
      "Leave bank balances",
      "Screenshots with dates visible",
    ],
    { x: 1.08, y: 4.22, w: 5.25 },
    { fontSize: 19, paraSpaceAfter: 5 }
  );
  addCard(slide, 7.0, 4.05, 4.25, 1.45, { fill: theme.white, lineColor: theme.borderSoft, shadow: false });
  slide.addText("If something looks wrong, report it to our union even if HR or OSU support is already working it.", {
    x: 7.35,
    y: 4.23,
    w: 3.4,
    h: 0.48,
    fontFace: theme.bodyFont,
    fontSize: 16,
    color: theme.text,
    align: "center",
    bold: true,
    margin: 0,
  });
  addPill(slide, "083stewards@seiu503.org", 7.45, 4.92, 3.25, { fill: theme.purpleLight, lineColor: theme.purpleLight, fontSize: 12.5, h: 0.52 });
  addFooter(slide);
  finalize(slide, pptx);
}

function rallySlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide, theme.purpleDark);
  if (fs.existsSync(fistsPath)) {
    slide.addImage({ path: fistsPath, ...imageSizingCrop(fistsPath, 0, 0, 13.333, 7.5) });
    slide.addShape("rect", { x: 0, y: 0, w: 13.333, h: 7.5, line: { color: theme.purpleDark, transparency: 100 }, fill: { color: theme.purpleDark, transparency: 42 } });
  }
  slide.addText("June 30: Rally for our Future", {
    x: 0.88,
    y: 1.02,
    w: 7.8,
    h: 1.05,
    fontFace: theme.headFont,
    fontSize: 44,
    bold: true,
    color: theme.white,
    margin: 0,
    fit: "shrink",
  });
  slide.addText("Tuesday, June 30, 2026 | Noon to 1 p.m. | McNary Field", {
    x: 0.92,
    y: 2.28,
    w: 6.8,
    h: 0.28,
    fontFace: theme.bodyFont,
    fontSize: 21,
    bold: true,
    color: "E9D5FF",
    margin: 0,
  });
  addCard(slide, 0.92, 3.15, 5.8, 2.08, { fill: theme.white, lineColor: theme.white, shadow: false });
  addBulletList(
    slide,
    ["Food and lawn games", "Wear purple", "Bring one coworker", "Show management we care"],
    { x: 1.25, y: 3.47, w: 4.9 },
    { fontSize: 18.5, paraSpaceAfter: 2, color: theme.text }
  );
  addCard(slide, 8.16, 2.62, 3.55, 3.9, { fill: theme.white, lineColor: theme.white, shadow: false });
  if (fs.existsSync(rallyQrPath)) {
    slide.addImage({ path: rallyQrPath, ...imageSizingContain(rallyQrPath, 8.55, 2.92, 2.78, 2.78) });
  }
  slide.addText("local083.org/rally", {
    x: 8.38,
    y: 5.86,
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

function closingSlide(pptx) {
  const slide = pptx.addSlide();
  addBackground(slide);
  addHeader(slide, 11, "Next steps");
  addTitle(slide, "How we show management we care", "The meeting ends with action. Pick the next step you can take today.", { subtitleSize: 18 });
  const actions = [
    "Show up and stay visible",
    "Bring coworkers into the conversation",
    "Become a full member",
    "Save Workday records before transition",
    "Sign up for the Rally for our Future",
  ];
  actions.forEach((action, index) => {
    const y = 2.65 + index * 0.62;
    slide.addText(String(index + 1), {
      x: 1.03,
      y: y + 0.05,
      w: 0.34,
      h: 0.13,
      fontFace: theme.bodyFont,
      fontSize: 13,
      bold: true,
      color: theme.white,
      align: "center",
      margin: 0,
      fill: { color: theme.purpleMid },
    });
    slide.addText(action, {
      x: 1.58,
      y,
      w: 5.6,
      h: 0.26,
      fontFace: theme.bodyFont,
      fontSize: 20,
      bold: true,
      color: theme.text,
      margin: 0,
    });
  });
  addCard(slide, 7.55, 2.65, 4.2, 1.8, { fill: theme.purplePale, lineColor: theme.purpleLight, shadow: false });
  slide.addText("Contact paths", {
    x: 7.9,
    y: 2.98,
    w: 3.0,
    h: 0.2,
    fontFace: theme.headFont,
    fontSize: 23,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
  });
  slide.addText("083execteam@seiu503.org\n083stewards@seiu503.org", {
    x: 7.9,
    y: 3.48,
    w: 3.55,
    h: 0.46,
    fontFace: theme.bodyFont,
    fontSize: 15,
    bold: true,
    color: theme.text,
    margin: 0,
    breakLine: false,
  });
  addCard(slide, 0.9, 5.85, 10.85, 0.62, { fill: theme.purpleDark, lineColor: theme.purpleDark, shadow: false });
  slide.addText("In solidarity, SEIU Local 503 Sublocal 083", {
    x: 1.25,
    y: 6.06,
    w: 10.0,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 16,
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
  pptx.subject = "Membership meeting deck for May 21, 2026";
  pptx.title = "Membership Meeting May 21 2026";
  pptx.company = "SEIU Local 503 at Oregon State University";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: theme.headFont,
    bodyFontFace: theme.bodyFont,
    lang: "en-US",
  };

  titleSlide(pptx);
  agendaSlide(pptx);
  introductionSlide(pptx);
  bargainingContextSlide(pptx);
  sideBySideSlide(pptx);
  bargainingDelegateSlide(pptx);
  membershipSlide(pptx);
  jamesPavisSlide(pptx);
  workdaySlide(pptx);
  rallySlide(pptx);
  closingSlide(pptx);

  await pptx.writeFile({ fileName: PPTX_PATH });
  console.log(PPTX_PATH);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
