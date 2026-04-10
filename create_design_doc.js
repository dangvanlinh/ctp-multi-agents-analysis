const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const hdrBorder = { style: BorderStyle.SINGLE, size: 1, color: "1E2761" };
const hdrBorders = { top: hdrBorder, bottom: hdrBorder, left: hdrBorder, right: hdrBorder };
const margins = { top: 80, bottom: 80, left: 120, right: 120 };

// Page width: US Letter 12240 - 2880 margins = 9360
const PAGE_W = 9360;

function hdr(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ heading: level, children: [new TextRun({ text, bold: true })] });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 120 },
    indent: opts.indent ? { left: opts.indent } : undefined,
    children: [new TextRun({ text, bold: opts.bold, italics: opts.italic, size: opts.size || 24, color: opts.color })]
  });
}

function bulletItem(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    children: [new TextRun({ text, size: 22 })]
  });
}

function numItem(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    children: [new TextRun({ text, size: 22 })]
  });
}

function makeRow(cells, isHeader = false) {
  return new TableRow({
    children: cells.map((text, i) => new TableCell({
      borders: isHeader ? hdrBorders : borders,
      margins,
      width: { size: Math.floor(PAGE_W / cells.length), type: WidthType.DXA },
      shading: isHeader
        ? { fill: "1E2761", type: ShadingType.CLEAR }
        : { fill: "FFFFFF", type: ShadingType.CLEAR },
      children: [new Paragraph({
        children: [new TextRun({
          text: String(text),
          bold: isHeader,
          color: isHeader ? "FFFFFF" : "1E1E2E",
          size: isHeader ? 20 : 20,
        })]
      })]
    }))
  });
}

function makeTable(headers, rows, colWidths) {
  const widths = colWidths || headers.map(() => Math.floor(PAGE_W / headers.length));
  return new Table({
    width: { size: PAGE_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({
        children: headers.map((h, i) => new TableCell({
          borders: hdrBorders, margins,
          width: { size: widths[i], type: WidthType.DXA },
          shading: { fill: "1E2761", type: ShadingType.CLEAR },
          children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: "FFFFFF", size: 20 })] })]
        }))
      }),
      ...rows.map((row, r) => new TableRow({
        children: row.map((cell, i) => new TableCell({
          borders, margins,
          width: { size: widths[i], type: WidthType.DXA },
          shading: { fill: r % 2 === 0 ? "F5F5F7" : "FFFFFF", type: ShadingType.CLEAR },
          children: [new Paragraph({ children: [new TextRun({ text: String(cell), size: 20 })] })]
        }))
      }))
    ]
  });
}

function edgeCase(title, options, chosen, pro, con, reason) {
  return [
    new Paragraph({
      spacing: { before: 200, after: 80 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: "DDDDDD", space: 4 } },
      children: [new TextRun({ text: title, bold: true, size: 24, color: "1E2761" })]
    }),
    para(`Options: ${options}`, { size: 20, color: "666666" }),
    para(`Chốt: ${chosen}`, { size: 22, bold: true, color: "2EA06A" }),
    para(`Pro: ${pro}`, { size: 20, indent: 360 }),
    para(`Con: ${con}`, { size: 20, indent: 360 }),
    para(`Lý do: ${reason}`, { size: 20, italic: true, indent: 360 }),
  ];
}

function spacer() {
  return new Paragraph({ spacing: { after: 200 }, children: [] });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1E2761" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "1E2761" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
        ] },
      { reference: "numbers",
        levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        ] },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: "1E2761", space: 4 } },
          children: [
            new TextRun({ text: "VIP Level System \u2014 Design Doc", size: 18, color: "999999", font: "Arial" }),
            new TextRun({ text: "\t\tDraft \u2014 2026-04-06", size: 18, color: "999999", font: "Arial" }),
          ],
          tabStops: [{ type: "right", position: 9360 }],
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, color: "999999" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "999999" }),
          ]
        })]
      })
    },
    children: [
      // ═══ TITLE ═══
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "VIP LEVEL SYSTEM", size: 52, bold: true, color: "1E2761", font: "Arial" })]
      }),
      new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({ text: "Design Document for Development", size: 28, color: "666666" })]
      }),
      new Paragraph({
        spacing: { after: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "E63E31", space: 8 } },
        children: [new TextRun({ text: "Status: Draft | Date: 2026-04-06 | UI Mockup: vip_ui_mockup.html", size: 20, color: "999999" })]
      }),

      // ═══ 1. OVERVIEW ═══
      hdr("1. Overview"),
      para("Redesign VIP t\u1EEB subscription \u0111\u01A1n gi\u1EA3n (100k/10 ng\u00E0y, 82.8% mua 1 l\u1EA7n) th\u00E0nh h\u1EC7 th\u1ED1ng level progression v\u1EDBi loss aversion."),
      spacer(),
      para("Core Pillars:", { bold: true, size: 24 }),
      numItem("Fix 2 v\u1EA5n \u0111\u1EC1 VIP: repay trong th\u00E1ng (ARPT 1\u21923) + repay th\u00E1ng sau (repeat 17%\u219250%)"),
      numItem("Kh\u00F4ng c\u1EAFn nhau v\u1EDBi event \u0111ang ch\u1EA1y (SKB, CH\u0110, Tr\u1EE9ng, Lazer)"),

      // ═══ 2. CORE MECHANIC ═══
      hdr("2. Core Mechanic"),
      makeTable(["Rule", "Chi ti\u1EBFt"], [
        ["S\u1ED1 c\u1EA5p", "5 c\u1EA5p (Lv1-Lv5)"],
        ["Gi\u00E1", "100k VN\u0110 / 10 ng\u00E0y (t\u1EA5t c\u1EA3 level)"],
        ["Level up", "Mua li\u00EAn ti\u1EBFp = +1 Level"],
        ["Reset", "Kh\u00F4ng mua + h\u1EBFt 3 ng\u00E0y grace = Reset v\u1EC1 Lv0"],
        ["Hi\u1EC3n th\u1ECB", "Ch\u1EC9 th\u1EA5y benefit level ti\u1EBFp theo +1, level xa b\u1ECB \u1EA9n"],
      ], [2500, 6860]),

      // ═══ 3. CONFIG BENEFIT ═══
      hdr("3. Config Benefit"),
      para("Gi\u00E1: 100k/10 ng\u00E0y t\u1EA5t c\u1EA3 level. Benefit t\u00EDch l\u0169y c\u1ED9ng d\u1ED3n.", { italic: true, color: "666666" }),
      spacer(),
      makeTable(
        ["Lv", "GEM", "R.V\u00E0ng", "Ch\u00ECa", "R.T\u00EDm", "EXP", "R.Cam", "Cosmetic", "DKXX", "Upg R", "Bonus%G"],
        [
          ["1", "1,500G", "50", "10", "5", "\u2014", "5", "Khung+FX Vip1", "\u2014", "\u2014", "TBD"],
          ["2", "1,500G", "50", "10", "10", "x2", "5", "Khung+FX Vip2", "+3%", "\u2014", "TBD"],
          ["3", "1,500G", "50", "10", "15", "x3", "10", "Khung+FX Vip3", "+5%", "Unlock", "TBD"],
          ["4", "1,500G", "50", "10", "20", "x3", "10", "Khung+FX Vip4", "+8%", "+10%", "TBD"],
          ["5", "1,500G", "50", "10", "30", "x4", "15", "Frame lobby", "+10%", "+15%", "TBD"],
        ],
        [400, 800, 700, 550, 650, 500, 650, 1500, 650, 700, 850]
      ),
      spacer(),
      para("Bonus %G: Ch\u01B0a ch\u1ED1t design. C\u1EA7n gi\u1EA3i quy\u1EBFt migration t\u1EEB shop trung. Xem m\u1EE5c 9.", { bold: true, color: "E63E31" }),

      // ═══ 4. BENEFIT DELIVERY ═══
      hdr("4. Benefit Delivery \u2014 2 Lo\u1EA1i"),

      hdr("4.1 Daily Claim (ph\u1EA3i login nh\u1EADn)", HeadingLevel.HEADING_2),
      para("Kh\u00F4ng login = m\u1EA5t qu\u00E0 ng\u00E0y \u0111\u00F3. M\u1EE5c \u0111\u00EDch: k\u00EDch new user login h\u00E0ng ng\u00E0y \u2192 t\u0103ng retention."),
      bulletItem("GEM (83G/ng\u00E0y)"),
      bulletItem("R\u01B0\u01A1ng v\u00E0ng (5/ng\u00E0y)"),
      bulletItem("R\u01B0\u01A1ng t\u00EDm: chia \u0111\u1EC1u 10 ng\u00E0y"),
      bulletItem("R\u01B0\u01A1ng cam: chia cho 5 ng\u00E0y cu\u1ED1i (ng\u00E0y 6-10)"),
      bulletItem("Ch\u00ECa kh\u00F3a: chia \u0111\u1EC1u 10 ng\u00E0y"),
      spacer(),
      para("VD Lv2 (10 t\u00EDm, 5 cam):", { bold: true }),
      makeTable(["Ng\u00E0y", "R.T\u00EDm", "R.Cam"], [
        ["1-5", "1/ng\u00E0y", "\u2014"],
        ["6-10", "1/ng\u00E0y", "1/ng\u00E0y"],
      ], [3120, 3120, 3120]),

      hdr("4.2 Auto-Active (mua VIP l\u00E0 c\u00F3)", HeadingLevel.HEADING_2),
      para("Whale c\u1EA7n buff khi ch\u01A1i, kh\u00F4ng c\u1EA7n login claim."),
      bulletItem("x2/x3/x4 EXP"),
      bulletItem("DKXX boost"),
      bulletItem("Upgrade R access"),
      bulletItem("Cosmetic (khung, FX)"),
      bulletItem("Bonus %G khi n\u1EA1p (n\u1EBFu ch\u1ED1t)"),
      spacer(),
      ...edgeCase(
        "Decision: Benefit delivery",
        "A) T\u1EA5t c\u1EA3 daily claim, B) T\u1EA5t c\u1EA3 auto-active, C) Chia 2 segment",
        "C \u2014 Chia 2 lo\u1EA1i theo segment",
        "New login h\u00E0ng ng\u00E0y, whale kh\u00F4ng b\u1ECB phi\u1EC1n",
        "Ph\u1EE9c t\u1EA1p h\u01A1n cho dev (2 lo\u1EA1i delivery)",
        "M\u1ED7i segment c\u00F3 behavior target kh\u00E1c nhau"
      ),

      // ═══ 5. TIMING ═══
      hdr("5. Timing & Countdown"),

      hdr("5.1 VIP t\u00EDnh theo ng\u00E0y", HeadingLevel.HEADING_2),
      bulletItem("Mua ng\u00E0y n\u00E0o th\u00EC h\u1EBFt 00:00 ng\u00E0y th\u1EE9 11"),
      bulletItem("Daily claim reset l\u00FAc 00:00"),
      spacer(),
      ...edgeCase(
        "Decision: Timezone",
        "A) T\u00EDnh theo gi\u1EDD ch\u00EDnh x\u00E1c, B) T\u00EDnh theo ng\u00E0y",
        "B \u2014 T\u00EDnh theo ng\u00E0y, reset 00:00",
        "D\u1EC5 hi\u1EC3u, align daily claim",
        "User mua 23:59 \u0111\u01B0\u1EE3c \u201Cfree\u201D g\u1EA7n 1 ng\u00E0y \u2014 negligible",
        "Simple cho user v\u00E0 dev, align v\u1EDBi daily system"
      ),

      hdr("5.2 Grace period", HeadingLevel.HEADING_2),
      bulletItem("H\u1EBFt 10 ng\u00E0y \u2192 user c\u00F3 3 ng\u00E0y \u0111\u1EC3 mua ti\u1EBFp"),
      bulletItem("Trong 3 ng\u00E0y: kh\u00F4ng qu\u00E0 daily, kh\u00F4ng buff auto-active"),
      bulletItem("Kh\u00F4ng mua trong 3 ng\u00E0y \u2192 reset Lv0"),
      spacer(),
      ...edgeCase(
        "Decision: Reset level",
        "A) Reset Lv0, B) Reset Lv3, C) Gi\u1EA3m 1 level/k\u1EF3",
        "A \u2014 Reset Lv0 (m\u1EA5t h\u1EBFt)",
        "Loss aversion m\u1EA1nh nh\u1EA5t, 50 ng\u00E0y effort + 500k m\u1EA5t tr\u1EAFng",
        "Harsh \u2014 nh\u01B0ng \u0111\u00F3 l\u00E0 point",
        "3 ng\u00E0y \u0111\u1EE7 d\u00E0i \u0111\u1EC3 quy\u1EBFt \u0111\u1ECBnh, n\u1EBFu drop th\u00EC m\u1EC1m h\u01A1n c\u0169ng kh\u00F4ng gi\u1EEF"
      ),

      // ═══ 6. MUA VIP RULES ═══
      hdr("6. Mua VIP \u2014 Rules"),

      hdr("6.1 Mua tr\u01B0\u1EDBc h\u1EA1n", HeadingLevel.HEADING_2),
      para("Khi user mua VIP ti\u1EBFp trong khi VIP hi\u1EC7n t\u1EA1i ch\u01B0a h\u1EBFt:"),
      numItem("Nh\u1EADn tr\u1ECDn qu\u00E0 c\u00F2n l\u1EA1i c\u1EE7a level hi\u1EC7n t\u1EA1i v\u00E0o inbox ngay"),
      numItem("Level hi\u1EC7n t\u1EA1i k\u1EBFt th\u00FAc"),
      numItem("Level m\u1EDBi k\u00EDch ho\u1EA1t ngay, 10 ng\u00E0y m\u1EDBi b\u1EAFt \u0111\u1EA7u"),
      spacer(),
      ...edgeCase(
        "Decision: Mua tr\u01B0\u1EDBc h\u1EA1n",
        "A) \u0110\u1EE3i h\u1EBFt k\u1EF3 m\u1EDBi l\u00EAn, B) L\u00EAn ngay m\u1EA5t ng\u00E0y c\u0169, C) Nh\u1EADn h\u1EBFt qu\u00E0 + l\u00EAn ngay",
        "C \u2014 Nh\u1EADn h\u1EBFt qu\u00E0 c\u00F2n l\u1EA1i + l\u00EAn level ngay",
        "User kh\u00F4ng m\u1EA5t g\u00EC, l\u00EAn level ngay, k\u00EDch mua s\u1EDBm = t\u0103ng ARPT",
        "Burst qu\u00E0 g\u1ED9p \u2014 nh\u01B0ng l\u00E0 qu\u00E0 \u0111\u00E1ng l\u1EBD nh\u1EADn r\u1ED3i",
        "T\u1EA1o incentive mua s\u1EDBm, user experience t\u1ED1t nh\u1EA5t"
      ),

      hdr("6.2 Mua nhi\u1EC1u l\u1EA7n li\u1EC1n", HeadingLevel.HEADING_2),
      bulletItem("Kh\u00F4ng cho ph\u00E9p mua nhi\u1EC1u l\u1EA7n c\u00F9ng l\u00FAc \u0111\u1EC3 nh\u1EA3y level"),
      bulletItem("B\u1EAFt bu\u1ED9c 1 l\u1EA7n mua = 1 level"),
      bulletItem("Nh\u1EA3y level ch\u1EC9 d\u00E0nh cho offer new user / lapsed"),
      spacer(),
      ...edgeCase(
        "Decision: Mua nhi\u1EC1u l\u1EA7n",
        "A) Cho nh\u1EA3y level, B) 1 l\u1EA7n = 1 level",
        "B \u2014 B\u1EAFt bu\u1ED9c mua t\u1EEBng level",
        "User tr\u1EA3i nghi\u1EC7m t\u1EEBng level, attach d\u1EA7n, loss aversion m\u1EA1nh",
        "Whale kh\u00F4ng fast-track \u2014 nh\u01B0ng \u0111\u00F3 l\u00E0 intent",
        "Spirit thi\u1EBFt k\u1EBF l\u00E0 progression t\u1EEBng b\u01B0\u1EDBc"
      ),

      // ═══ 7. NÚT KÍCH HOẠT ═══
      hdr("7. N\u00FAt K\u00EDch Ho\u1EA1t \u2014 State Machine"),
      para("Rule: Ch\u01B0a claim qu\u00E0 h\u00F4m nay \u2192 ch\u01B0a cho renew.", { bold: true, color: "E63E31" }),
      spacer(),
      makeTable(
        ["Tr\u1EA1ng th\u00E1i", "N\u00FAt Claim", "N\u00FAt K\u00EDch ho\u1EA1t"],
        [
          ["Ch\u01B0a l\u00E0 VIP", "Kh\u00F4ng c\u00F3", "Hi\u1EC7n (mua l\u1EA7n \u0111\u1EA7u)"],
          ["\u0110ang VIP, >3 ng\u00E0y, ch\u01B0a claim", "Hi\u1EC7n", "\u1EA8n"],
          ["\u0110ang VIP, >3 ng\u00E0y, \u0111\u00E3 claim", "Kh\u00F4ng", "\u1EA8n"],
          ["\u0110ang VIP, \u22643 ng\u00E0y, ch\u01B0a claim", "Hi\u1EC7n", "\u1EA8n (ch\u1EDD claim)"],
          ["\u0110ang VIP, \u22643 ng\u00E0y, \u0111\u00E3 claim", "Kh\u00F4ng", "Hi\u1EC7n (renew)"],
          ["H\u1EBFt VIP, trong 3 ng\u00E0y grace", "Kh\u00F4ng", "Hi\u1EC7n (urgent)"],
          ["H\u1EBFt VIP, qu\u00E1 3 ng\u00E0y \u2192 Lv0", "Kh\u00F4ng", "Hi\u1EC7n (mua l\u1EA1i Lv1)"],
        ],
        [4000, 2500, 2860]
      ),

      // ═══ 8. UPGRADE R ═══
      hdr("8. Upgrade R"),
      makeTable(["Rule", "Chi ti\u1EBFt"], [
        ["Hi\u1EC7n t\u1EA1i", "Ch\u1EC9 CLB h\u1EA1ng B+ m\u1EDBi upgrade R"],
        ["M\u1EDBi", "VIP Lv3+ c\u0169ng unlock Upgrade R (m\u1EDF th\u00EAm \u0111\u01B0\u1EDDng)"],
        ["VIP h\u1EBFt", "Kh\u00F3a ngay quy\u1EC1n Upgrade R"],
        ["Th\u1EBB R \u0111\u00E3 upgrade", "Gi\u1EEF nguy\u00EAn, kh\u00F4ng revert"],
        ["CLB B + VIP", "Bonus rate c\u1ED9ng d\u1ED3n"],
      ], [2500, 6860]),
      spacer(),
      makeTable(["Level", "Upgrade R", "M\u00F4 t\u1EA3"], [
        ["Lv1-2", "\u2014", "Kh\u00F4ng c\u00F3"],
        ["Lv3", "Unlock", "M\u1EDF quy\u1EC1n upgrade R"],
        ["Lv4", "+10% rate", "T\u0103ng t\u1EF7 l\u1EC7 th\u00E0nh c\u00F4ng"],
        ["Lv5", "+15% rate", "T\u1EF7 l\u1EC7 cao nh\u1EA5t"],
      ], [2000, 2500, 4860]),

      // ═══ 9. CHƯA CHỐT ═══
      hdr("9. Ch\u01B0a Ch\u1ED1t \u2014 C\u1EA7n Design Th\u00EAm"),

      hdr("9.1 Bonus %G (PARKED)", HeadingLevel.HEADING_2),
      bulletItem("Shop trung hi\u1EC7n cho bonus 5-20% free theo g\u00F3i (50k\u21925%, 1M\u219220%)"),
      bulletItem("65% GEM payer ch\u01B0a mua VIP \u2192 n\u1EBFu remove shop bonus, h\u1ECD m\u1EA5t h\u1EBFt"),
      bulletItem("81% transactions l\u00E0 g\u00F3i \u2264200k (bonus \u226410%)"),
      bulletItem("H\u01B0\u1EDBng xem x\u00E9t: Gi\u1EEF shop 10% flat, VIP c\u1ED9ng th\u00EAm +5%/level"),
      bulletItem("Blocker: C\u1EA7n t\u00EDnh balance k\u1EF9 h\u01A1n, concern v\u1EC1 GEM inflation"),

      hdr("9.2 Lapsed Rule (PARKED)", HeadingLevel.HEADING_2),
      bulletItem("Offer skip Lv2 cho lapsed user c\u00F3 th\u1EC3 b\u1ECB gaming"),
      bulletItem("Ch\u1EDD data live v\u1EC1 lapsed behavior r\u1ED3i m\u1EDBi design"),
      bulletItem("Default: lapsed mua l\u1EA1i = Lv1, kh\u00F4ng KM"),

      hdr("9.3 New User Offer (PARKED)", HeadingLevel.HEADING_2),
      bulletItem("L\u1EA7n mua \u0111\u1EA7u ti\u00EAn trong \u0111\u1EDDi \u2192 skip l\u00EAn Lv2 ngay"),
      bulletItem("C\u1EA7n design offer UI ri\u00EAng"),

      // ═══ 10. UI ═══
      hdr("10. UI Screens"),

      hdr("10.1 Screens \u0111\u00E3 mockup", HeadingLevel.HEADING_2),
      para("File: vip_ui_mockup.html", { italic: true, color: "666666" }),
      numItem("Ch\u01B0a VIP \u2014 preview Lv1, n\u00FAt K\u00EDch ho\u1EA1t, benefit m\u1EDD"),
      numItem("\u0110ang VIP \u2014 benefit s\u00E1ng, n\u00FAt Claim qu\u00E0, countdown, arrows xem level"),
      numItem("VIP \u22643 ng\u00E0y \u2014 urgent, Claim + Renew (disabled \u0111\u1EBFn khi claim)"),
      numItem("H\u1EBFt VIP \u2014 3 ng\u00E0y grace, t\u1EA5t c\u1EA3 kh\u00F3a, urgent"),

      hdr("10.2 Arrow Navigation", HeadingLevel.HEADING_2),
      bulletItem("Tr\u00E1i: xem l\u1EA1i level \u0111\u00E3 qua"),
      bulletItem("Ph\u1EA3i: ch\u1EC9 t\u1EDBi level hi\u1EC7n t\u1EA1i +1, ti\u1EBFp theo \u201C???\u201D"),
      bulletItem("Lv5 ph\u1EA3i: \u201CMax Level\u201D"),

      hdr("10.3 C\u1EA7n design th\u00EAm", HeadingLevel.HEADING_2),
      bulletItem("Redesign n\u00FAt VIP \u1EDF bottom bar main screen"),
      bulletItem("New user offer popup"),
      bulletItem("Ref art th\u1EBB VIP c\u00E1c c\u1EA5p (Lv1-5)"),
      bulletItem("Ref khung qu\u00E0 trong UI VIP"),
      bulletItem("Ref cosmetic: khung avatar, FX tung XX, khung deco NV lobby, BG lobby"),

      // ═══ 11. NOTI ═══
      hdr("11. Noti/Communication"),
      bulletItem("Kh\u00F4ng push noti \u2014 d\u00F9ng in-game UI khi login"),
      bulletItem("Daily claim popup = touchpoint t\u1EF1 nhi\u00EAn \u0111\u1EC3 nh\u1EAFc countdown VIP"),
      bulletItem("User kh\u00F4ng login \u2192 kh\u00F4ng bi\u1EBFt VIP s\u1EAFp h\u1EBFt"),

      // ═══ 12. KPI ═══
      hdr("12. KPI Target"),
      para("Rev target: 350tr+/th\u00E1ng (hi\u1EC7n ~72tr)", { bold: true, size: 26, color: "1E2761" }),
      para("Model: 800 PU m\u1EDBi, new retain 50%, old retain 80%, new ARPT=2, old ARPT=3", { color: "666666" }),
      spacer(),
      makeTable(
        ["Th\u00E1ng", "PU m\u1EDBi", "Old retained", "Active PU", "L\u01B0\u1EE3t", "Rev"],
        [
          ["T1", "800", "362", "1,162", "2,686", "269M"],
          ["T2", "800", "690", "1,490", "3,670", "367M"],
          ["T3", "800", "952", "1,752", "4,456", "446M"],
          ["T4", "800", "1,162", "1,962", "5,086", "509M"],
          ["T6+", "800", "~2,000", "~2,800", "~7,600", "~760M"],
        ],
        [1200, 1200, 1700, 1500, 1500, 1260]
      ),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("D:\\Work\\VNG\\ctp1\\Agent\\ctp-multi-agents-analysis\\data\\VIP_Design_Doc_v1.docx", buffer);
  console.log("Saved: data/VIP_Design_Doc_v1.docx");
});
