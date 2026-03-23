"use strict";

const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");
const {
  autoFontSize,
  calcTextBox,
  imageSizingContain,
  safeOuterShadow,
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers");

const ROOT = __dirname;
const OUT_DIR = path.join(ROOT, "output");
const PPTX_PATH = path.join(OUT_DIR, "membership-meeting-template.pptx");
const logoPath = path.resolve(ROOT, "../../images/logo.png");

const theme = {
  purpleDark: "4C1D95",
  purple: "7C3AED",
  purpleMid: "6D28D9",
  purpleLight: "EDE9FE",
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
  marginX: 0.92,
  contentW: 11.49,
  headerY: 0.46,
  headerRuleY: 0.9,
  titleY: 1.32,
  introY: 1.92,
  footerY: 7.02,
  cardRadius: 0.1,
  cardShadow: safeOuterShadow("000000", 0.1, 45, 1.5, 1),
};

const sample = {
  label: "SEIU Local 503 at Oregon State University",
  title: "Membership Meeting Template",
  subtitle:
    "Campaign-forward slides for updates, turnout asks, and practical meeting logistics.",
  details: [
    "Thursday, April 16, 2026",
    "Noon to 1 p.m.",
    "MU 211",
    "RSVP workflow active",
  ],
  agenda: [
    "Welcome and what members need first",
    "Current union updates and key decisions ahead",
    "Discussion on workplace priorities and member questions",
    "Upcoming actions, events, and turnout asks",
    "RSVP, contacts, and next steps",
  ],
  updateTitle: "Key update example",
  updateBody:
    "Our membership meeting is where we share the latest updates, hear directly from members, and move our union forward together. The main update slide should hold one lead message, a short explanation, and one concrete member action.",
  highlights: [
    "Use exact dates, locations, and next actions.",
    "Keep the turnout ask visible on dense slides.",
    "Write in our union voice: we, us, and our members.",
  ],
  discussionLeft: [
    "What members are hearing in departments",
    "Questions that need follow-up after the meeting",
    "Issues that need clearer contract-campaign framing",
  ],
  discussionRight: [
    "What we need members to do next",
    "Who should RSVP or join on Zoom",
    "Which updates belong in the next follow-up email",
  ],
  logistics: [
    { label: "Date", value: "Thursday, April 16, 2026" },
    { label: "Time", value: "Noon to 1 p.m." },
    { label: "In person", value: "MU 211" },
    { label: "Online", value: "Zoom details added to RSVP confirmation" },
  ],
  ctaTitle: "Make the next action obvious",
  ctaBody:
    "Use this slide when everyone in the room should leave with one specific next step. The action needs to be clear enough to read in seconds and easy enough to repeat out loud.",
  ctaButton: "RSVP now",
  ctaLink: "forms.cloud.microsoft/.../membership-meeting-rsvp",
  ctaReasons: [
    "Helps us plan food orders and turnout",
    "Delivers the calendar invite right away",
    "Makes the ask concrete and measurable",
  ],
  closing:
    "Thank members, restate the next action, and close with one clean contact path for questions or steward support.",
};

fs.mkdirSync(OUT_DIR, { recursive: true });

function addFullBackground(slide, color = theme.light) {
  slide.background = { color };
}

function addHeader(slide, pageNum, section = "Membership meeting template") {
  slide.addText(sample.label, {
    x: layout.marginX,
    y: layout.headerY,
    w: 6.5,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 9.5,
    bold: true,
    color: theme.purpleDark,
    margin: 0,
    charSpace: 0.3,
  });
  slide.addText(section, {
    x: 8.6,
    y: layout.headerY,
    w: 3.0,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 9,
    color: theme.muted,
    align: "right",
    margin: 0,
  });
  slide.addText(String(pageNum).padStart(2, "0"), {
    x: 11.9,
    y: layout.headerY,
    w: 0.5,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 9,
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
  slide.addText("SEIU Local 083 membership meeting slide system", {
    x: layout.marginX,
    y: layout.footerY,
    w: 4.0,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 8,
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
    fill: { color: opts.fill || theme.white },
    shadow: opts.shadow === false ? undefined : layout.cardShadow,
  });
}

function addSectionLead(slide, title, subtitle) {
  const titleBox = { x: layout.marginX, y: layout.titleY, w: 7.8, h: 0.52 };
  slide.addText(title, {
    ...autoFontSize(title, theme.headFont, {
      x: titleBox.x,
      y: titleBox.y,
      w: titleBox.w,
      h: titleBox.h,
      fontSize: 24,
      minFontSize: 18,
      maxFontSize: 28,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });
  const sub = calcTextBox(13.5, {
    text: subtitle,
    w: 8.2,
    fontFace: theme.bodyFont,
    margin: 0,
  });
  slide.addText(subtitle, {
    x: layout.marginX,
    y: layout.introY,
    w: 8.2,
    h: sub.h,
    fontFace: theme.bodyFont,
    fontSize: 13.5,
    color: theme.textSecondary,
    margin: 0,
  });
}

function addBulletList(slide, items, box, fontSize = 15, opts = {}) {
  const runs = [];
  items.forEach((item, index) => {
    runs.push({
      text: item,
      options: {
        bullet: { indent: opts.indent || 18 },
        breakLine: index < items.length - 1,
      },
    });
  });
  const measured = calcTextBox(fontSize, {
    text: runs,
    w: box.w,
    fontFace: theme.bodyFont,
    margin: 0,
    paraSpaceAfter: opts.paraSpaceAfter || 6,
  });
  slide.addText(runs, {
    x: box.x,
    y: box.y,
    w: box.w,
    h: measured.h,
    fontFace: theme.bodyFont,
    fontSize,
    color: opts.color || theme.text,
    margin: 0,
    paraSpaceAfter: opts.paraSpaceAfter || 6,
    valign: "top",
  });
}

function addMetaPills(slide, items, startY) {
  let x = layout.marginX;
  items.forEach((item) => {
    const w = Math.max(1.25, Math.min(2.8, 0.6 + item.length * 0.07));
    slide.addShape("roundRect", {
      x,
      y: startY,
      w,
      h: 0.38,
      rectRadius: 0.08,
      line: { color: theme.border, pt: 1 },
      fill: { color: theme.white },
    });
    slide.addText(item, {
      x: x + 0.14,
      y: startY + 0.11,
      w: w - 0.28,
      h: 0.14,
      fontFace: theme.bodyFont,
      fontSize: 10.5,
      color: theme.textSecondary,
      margin: 0,
      align: "center",
    });
    x += w + 0.14;
  });
}

function addCompactLabel(slide, text, x, y, w, color = theme.purpleMid) {
  slide.addText(text, {
    x,
    y,
    w,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 9.5,
    bold: true,
    color,
    margin: 0,
    charSpace: 0.25,
  });
}

function finalizeSlide(slide, pptx, opts = {}) {
  if (!opts.skipOverlapCheck) {
    warnIfSlideHasOverlaps(slide, pptx, { muteContainment: true });
  }
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

function buildTitleSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);

  slide.addShape("rect", {
    x: layout.marginX,
    y: 1.08,
    w: 0.08,
    h: 4.9,
    line: { color: theme.purpleDark, transparency: 100 },
    fill: { color: theme.purpleDark },
  });

  slide.addImage({
    path: logoPath,
    ...imageSizingContain(logoPath, 10.52, 1.12, 1.15, 1.15),
  });
  slide.addText("SEIU Local 083", {
    x: 9.45,
    y: 2.48,
    w: 2.6,
    h: 0.2,
    fontFace: theme.bodyFont,
    fontSize: 10,
    bold: true,
    color: theme.purpleDark,
    align: "right",
    margin: 0,
  });

  slide.addText(sample.title, {
    ...autoFontSize(sample.title, theme.headFont, {
      x: 1.28,
      y: 1.46,
      w: 7.4,
      h: 0.86,
      fontSize: 30,
      minFontSize: 24,
      maxFontSize: 34,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });

  const subtitle = calcTextBox(17, {
    text: sample.subtitle,
    w: 6.7,
    fontFace: theme.bodyFont,
    margin: 0,
  });
  slide.addText(sample.subtitle, {
    x: 1.28,
    y: 2.55,
    w: 6.7,
    h: subtitle.h,
    fontFace: theme.bodyFont,
    fontSize: 17,
    color: theme.textSecondary,
    margin: 0,
  });

  addMetaPills(slide, sample.details, 3.62);

  addCard(slide, 1.28, 4.44, 8.5, 1.18, {
    fill: theme.white,
    lineColor: theme.borderSoft,
    shadow: false,
  });
  addCompactLabel(slide, "Template structure", 1.54, 4.72, 2.1);
  slide.addText(
    "Built for membership updates, facilitation, turnout asks, logistics, and clean closing slides.",
    {
      x: 1.54,
      y: 5.0,
      w: 7.8,
      h: 0.32,
      fontFace: theme.bodyFont,
      fontSize: 16,
      color: theme.text,
      margin: 0,
    }
  );

  addHeader(slide, 1, "Opening");
  addFooter(slide);
  finalizeSlide(slide, pptx, { skipOverlapCheck: true });
}

function buildAgendaSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);
  addHeader(slide, 2, "Agenda");
  addSectionLead(
    slide,
    "Agenda slide",
    "Use a simple, readable stack. The room should understand the sequence in seconds."
  );

  let y = 2.76;
  sample.agenda.forEach((item, index) => {
    addCard(slide, layout.marginX, y, 10.0, 0.72, {
      fill: theme.white,
      lineColor: theme.borderSoft,
      shadow: false,
    });
    slide.addShape("roundRect", {
      x: 1.14,
      y: y + 0.18,
      w: 0.38,
      h: 0.36,
      rectRadius: 0.07,
      line: { color: theme.purpleLight, transparency: 100 },
      fill: { color: index === 0 ? theme.purpleDark : theme.purpleLight },
    });
    slide.addText(String(index + 1), {
      x: 1.14,
      y: y + 0.26,
      w: 0.38,
      h: 0.12,
      fontFace: theme.bodyFont,
      fontSize: 9.5,
      bold: true,
      color: index === 0 ? theme.white : theme.purpleDark,
      align: "center",
      margin: 0,
    });
    slide.addText(item, {
      x: 1.78,
      y: y + 0.2,
      w: 8.5,
      h: 0.22,
      fontFace: theme.bodyFont,
      fontSize: 17,
      bold: index === 0,
      color: theme.text,
      margin: 0,
    });
    y += 0.84;
  });

  addCard(slide, 11.1, 2.76, 1.3, 1.9, {
    fill: theme.purpleLight,
    lineColor: theme.purpleLight,
    shadow: false,
  });
  slide.addText("Lead with logistics.\nEnd with action.", {
    x: 11.32,
    y: 3.08,
    w: 0.86,
    h: 1.15,
    fontFace: theme.headFont,
    fontSize: 16,
    color: theme.purpleDark,
    align: "center",
    margin: 0,
  });

  addFooter(slide);
  finalizeSlide(slide, pptx);
}

function buildSectionDividerSlide(pptx) {
  const slide = pptx.addSlide();
  slide.background = { color: theme.purpleDark };

  slide.addShape("rect", {
    x: layout.marginX,
    y: 1.46,
    w: 0.1,
    h: 2.8,
    line: { color: theme.white, transparency: 100 },
    fill: { color: theme.white },
  });
  slide.addText("Union updates", {
    x: 1.36,
    y: 1.7,
    w: 7.0,
    h: 0.74,
    fontFace: theme.headFont,
    fontSize: 32,
    bold: true,
    color: theme.white,
    margin: 0,
  });
  slide.addText(
    "Use divider slides to reset the room between logistics, updates, discussion, and next actions.",
    {
      x: 1.38,
      y: 2.7,
      w: 6.2,
      h: 0.56,
      fontFace: theme.bodyFont,
      fontSize: 17,
      color: "E9D5FF",
      margin: 0,
    }
  );
  slide.addText("One message.\nOne beat.\nMove on.", {
    x: 9.5,
    y: 2.0,
    w: 2.1,
    h: 1.3,
    fontFace: theme.bodyFont,
    fontSize: 18,
    bold: true,
    color: theme.white,
    align: "right",
    margin: 0,
  });
  slide.addText("03", {
    x: 11.85,
    y: 6.8,
    w: 0.5,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 9,
    color: "C4B5FD",
    align: "right",
    margin: 0,
  });
  finalizeSlide(slide, pptx);
}

function buildUpdateSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);
  addHeader(slide, 4, "Update");
  addSectionLead(
    slide,
    "Key update slide",
    "Use one lead message, one short explanation, and one compact support panel."
  );

  addCard(slide, layout.marginX, 2.82, 7.3, 3.08, {
    fill: theme.white,
    lineColor: theme.borderSoft,
    shadow: false,
  });
  addCompactLabel(slide, "Lead message", 1.16, 3.12, 1.6);
  slide.addText(sample.updateTitle, {
    ...autoFontSize(sample.updateTitle, theme.headFont, {
      x: 1.16,
      y: 3.36,
      w: 5.9,
      h: 0.44,
      fontSize: 23,
      minFontSize: 18,
      maxFontSize: 26,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });
  const updateBody = calcTextBox(16, {
    text: sample.updateBody,
    w: 6.2,
    fontFace: theme.bodyFont,
    margin: 0,
  });
  slide.addText(sample.updateBody, {
    x: 1.16,
    y: 4.0,
    w: 6.2,
    h: updateBody.h,
    fontFace: theme.bodyFont,
    fontSize: 16,
    color: theme.text,
    margin: 0,
  });

  addCard(slide, 8.52, 2.82, 3.89, 1.48, {
    fill: theme.purpleLight,
    lineColor: theme.purpleLight,
    shadow: false,
  });
  addCompactLabel(slide, "How to frame it", 8.82, 3.12, 2.0);
  sample.highlights.forEach((item, index) => {
    slide.addShape("roundRect", {
      x: 8.84,
      y: 3.46 + index * 0.23,
      w: 0.1,
      h: 0.1,
      rectRadius: 0.02,
      line: { color: theme.purpleMid, transparency: 100 },
      fill: { color: theme.purpleMid },
    });
    slide.addText(item, {
      x: 9.06,
      y: 3.39 + index * 0.23,
      w: 2.82,
      h: 0.16,
      fontFace: theme.bodyFont,
      fontSize: 9.2,
      color: theme.text,
      margin: 0,
    });
  });

  addCard(slide, 8.52, 4.64, 3.89, 1.26, {
    fill: theme.purpleDark,
    lineColor: theme.purpleDark,
    shadow: false,
  });
  slide.addText("Member action", {
    x: 8.82,
    y: 4.9,
    w: 1.5,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 9.5,
    bold: true,
    color: "DDD6FE",
    margin: 0,
  });
  slide.addText("Keep the RSVP or next turnout ask visible.", {
    x: 8.82,
    y: 5.18,
    w: 3.0,
    h: 0.34,
    fontFace: theme.bodyFont,
    fontSize: 15,
    bold: true,
    color: theme.white,
    margin: 0,
  });

  addFooter(slide);
  finalizeSlide(slide, pptx);
}

function buildTwoColumnSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);
  addHeader(slide, 5, "Discussion");
  addSectionLead(
    slide,
    "Two-column discussion slide",
    "Use equal-weight columns when you need to hold both member feedback and the asks that follow from it."
  );

  addCard(slide, layout.marginX, 2.82, 5.55, 3.16, {
    fill: theme.white,
    lineColor: theme.borderSoft,
    shadow: false,
  });
  addCard(slide, 6.86, 2.82, 5.55, 3.16, {
    fill: theme.white,
    lineColor: theme.borderSoft,
    shadow: false,
  });
  addCompactLabel(slide, "What we're hearing", 1.16, 3.12, 2.0);
  addCompactLabel(slide, "What we need from members", 7.1, 3.12, 2.3);
  addBulletList(slide, sample.discussionLeft, { x: 1.16, y: 3.46, w: 4.7 }, 15);
  addBulletList(slide, sample.discussionRight, { x: 7.1, y: 3.46, w: 4.7 }, 15);

  addFooter(slide);
  finalizeSlide(slide, pptx);
}

function buildLogisticsSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);
  addHeader(slide, 6, "Logistics");
  addSectionLead(
    slide,
    "Logistics slide",
    "Use a clean grid so date, time, location, and Zoom details are easy to scan quickly."
  );

  const positions = [
    [layout.marginX, 2.9],
    [3.86, 2.9],
    [6.8, 2.9],
    [9.74, 2.9],
  ];
  sample.logistics.forEach((item, index) => {
    const [x, y] = positions[index];
    addCard(slide, x, y, 2.68, 1.52, {
      fill: theme.white,
      lineColor: theme.borderSoft,
      shadow: false,
    });
    addCompactLabel(slide, item.label, x + 0.24, y + 0.22, 1.4, theme.muted);
    const bodyLayout = calcTextBox(14.5, {
      text: item.value,
      w: 2.18,
      fontFace: theme.bodyFont,
      margin: 0,
    });
    slide.addText(item.value, {
      x: x + 0.24,
      y: y + 0.56,
      w: 2.18,
      h: bodyLayout.h,
      fontFace: theme.bodyFont,
      fontSize: 14.5,
      color: theme.text,
      margin: 0,
    });
  });

  addCard(slide, layout.marginX, 4.88, 11.5, 0.92, {
    fill: theme.purpleLight,
    lineColor: theme.purpleLight,
    shadow: false,
  });
  addCompactLabel(slide, "Presenter note", 1.16, 5.15, 1.5);
  slide.addText(
    "If Zoom details or the agenda are still pending, say that directly and tell members where the update will appear next.",
    {
      x: 1.16,
      y: 5.42,
      w: 10.45,
      h: 0.22,
      fontFace: theme.bodyFont,
      fontSize: 13.5,
      color: theme.text,
      margin: 0,
    }
  );

  addFooter(slide);
  finalizeSlide(slide, pptx);
}

function buildCtaSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);
  addHeader(slide, 7, "Next action");

  slide.addShape("rect", {
    x: layout.marginX,
    y: 1.3,
    w: 0.1,
    h: 4.85,
    line: { color: theme.purpleDark, transparency: 100 },
    fill: { color: theme.purpleDark },
  });

  slide.addText(sample.ctaTitle, {
    ...autoFontSize(sample.ctaTitle, theme.headFont, {
      x: 1.3,
      y: 1.5,
      w: 6.2,
      h: 0.66,
      fontSize: 27,
      minFontSize: 21,
      maxFontSize: 30,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });

  const ctaBody = calcTextBox(16.5, {
    text: sample.ctaBody,
    w: 5.85,
    fontFace: theme.bodyFont,
    margin: 0,
  });
  slide.addText(sample.ctaBody, {
    x: 1.3,
    y: 2.4,
    w: 5.85,
    h: ctaBody.h,
    fontFace: theme.bodyFont,
    fontSize: 16.5,
    color: theme.text,
    margin: 0,
  });

  slide.addShape("roundRect", {
    x: 1.3,
    y: 4.62,
    w: 3.6,
    h: 0.72,
    rectRadius: 0.11,
    line: { color: theme.purpleDark, pt: 1 },
    fill: { color: theme.purpleDark },
  });
  slide.addText(sample.ctaButton, {
    x: 1.52,
    y: 4.86,
    w: 3.16,
    h: 0.16,
    fontFace: theme.bodyFont,
    fontSize: 17,
    bold: true,
    color: theme.white,
    align: "center",
    margin: 0,
  });
  slide.addText(sample.ctaLink, {
    x: 1.34,
    y: 5.56,
    w: 5.7,
    h: 0.14,
    fontFace: theme.bodyFont,
    fontSize: 10.5,
    color: theme.muted,
    margin: 0,
  });

  addCard(slide, 7.9, 1.62, 4.52, 4.18, {
    fill: theme.white,
    lineColor: theme.borderSoft,
    shadow: false,
  });
  addCompactLabel(slide, "Why this works", 8.22, 1.94, 1.8);
  addBulletList(slide, sample.ctaReasons, { x: 8.22, y: 2.34, w: 3.5 }, 15);

  addFooter(slide);
  finalizeSlide(slide, pptx);
}

function buildClosingSlide(pptx) {
  const slide = pptx.addSlide();
  addFullBackground(slide);
  addHeader(slide, 8, "Closing");

  slide.addImage({
    path: logoPath,
    ...imageSizingContain(logoPath, 1.02, 1.46, 0.92, 0.92),
  });
  slide.addText("Thank you for showing up", {
    ...autoFontSize("Thank you for showing up", theme.headFont, {
      x: 2.2,
      y: 1.52,
      w: 6.6,
      h: 0.62,
      fontSize: 28,
      minFontSize: 22,
      maxFontSize: 31,
      bold: true,
      color: theme.purpleDark,
      margin: 0,
      mode: "auto",
    }),
    fontFace: theme.headFont,
  });

  const closingLayout = calcTextBox(17, {
    text: sample.closing,
    w: 6.6,
    fontFace: theme.bodyFont,
    margin: 0,
  });
  slide.addText(sample.closing, {
    x: 2.2,
    y: 2.42,
    w: 6.6,
    h: closingLayout.h,
    fontFace: theme.bodyFont,
    fontSize: 17,
    color: theme.text,
    margin: 0,
  });

  addCard(slide, 1.02, 4.34, 7.8, 1.0, {
    fill: theme.purpleLight,
    lineColor: theme.purpleLight,
    shadow: false,
  });
  addCompactLabel(slide, "Close with", 1.3, 4.65, 1.2);
  slide.addText("one clear next action, one timeline, and one follow-up path.", {
    x: 1.3,
    y: 4.9,
    w: 6.7,
    h: 0.18,
    fontFace: theme.bodyFont,
    fontSize: 14,
    color: theme.text,
    margin: 0,
  });

  addCard(slide, 9.34, 1.52, 3.07, 3.82, {
    fill: theme.white,
    lineColor: theme.borderSoft,
    shadow: false,
  });
  addCompactLabel(slide, "Contact path", 9.64, 1.86, 1.5);
  slide.addText("083stewards@seiu503.org\n083execteam@seiu503.org", {
    x: 9.64,
    y: 2.26,
    w: 2.35,
    h: 0.82,
    fontFace: theme.bodyFont,
    fontSize: 14,
    color: theme.text,
    margin: 0,
  });
  addCompactLabel(slide, "Reusable close", 9.64, 3.44, 1.6);
  slide.addText("Restate the next action and where follow-up information will land.", {
    x: 9.64,
    y: 3.82,
    w: 2.28,
    h: 0.5,
    fontFace: theme.bodyFont,
    fontSize: 12.5,
    color: theme.textSecondary,
    margin: 0,
  });

  addFooter(slide);
  finalizeSlide(slide, pptx);
}

async function main() {
  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "OpenAI Codex";
  pptx.company = "SEIU Local 503 at Oregon State University";
  pptx.subject = "Membership meeting slide template";
  pptx.title = "SEIU Local 083 Membership Meeting Template";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: theme.headFont,
    bodyFontFace: theme.bodyFont,
    lang: "en-US",
  };
  pptx.defineSlideMaster({
    title: "SEIU083",
    background: { color: theme.light },
    margin: [0.35, 0.35, 0.35, 0.35],
  });

  buildTitleSlide(pptx);
  buildAgendaSlide(pptx);
  buildSectionDividerSlide(pptx);
  buildUpdateSlide(pptx);
  buildTwoColumnSlide(pptx);
  buildLogisticsSlide(pptx);
  buildCtaSlide(pptx);
  buildClosingSlide(pptx);

  await pptx.writeFile({ fileName: PPTX_PATH });
  console.log(`Wrote ${PPTX_PATH}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
