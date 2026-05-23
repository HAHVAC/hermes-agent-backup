---
name: vietnam-contract-review
description: Use this skill whenever the user asks to draft, create, review, redline, compare, risk-check, or negotiate Vietnamese contracts, especially hợp đồng lao động, hợp đồng kinh tế/thương mại/dịch vụ, hợp đồng thi công xây dựng/MEP/PCCC, hợp đồng giao khoán/khoán việc/khoán nhân công, phụ lục, nghiệm thu, thanh lý, hoặc checklist trước khi ký. This skill is for Vietnam-law-aware contract work and should be used even when the user only says “soát hợp đồng”, “kiểm tra hợp đồng”, “làm hợp đồng”, “điều khoản rủi ro”, “theo luật Việt Nam”, or uploads DOCX/PDF contract files.
---

# Vietnam Contract Review / Drafting Playbook

This skill helps draft and review Vietnamese-law contracts for business use. It is a decision-support workflow, not a substitute for a licensed lawyer. Be practical: identify risks, cite likely legal bases when known, propose safer wording, and surface business decisions the signer must make.

## Scope

Use for these first-class contract types:

1. **Hợp đồng lao động**: xác định thời hạn, không xác định thời hạn, thử việc, phụ lục HĐLĐ.
2. **Hợp đồng kinh tế / thương mại / dịch vụ / mua bán**.
3. **Hợp đồng thi công xây dựng / MEP / PCCC**: nhà thầu chính, thầu phụ, cung cấp-lắp đặt, bảo trì.
4. **Hợp đồng giao khoán / khoán việc / khoán nhân công**.
5. Related documents: phụ lục hợp đồng, biên bản nghiệm thu, thanh lý, bảo lãnh, cam kết bảo mật, checklist trước khi ký.

## First questions to resolve

If missing and the answer materially affects the review, ask concise questions before finalizing. If the user wants speed, proceed with assumptions and list them.

- Anh/khách hàng đang ở vị thế nào: bên thuê, bên nhận thầu, người sử dụng lao động, người lao động, nhà thầu chính, thầu phụ, bên mua, bên bán?
- Mục tiêu: soạn mới, rà soát rủi ro, redline đề xuất, tóm tắt nghĩa vụ, hay checklist trước khi ký?
- Giá trị hợp đồng, thời hạn, địa điểm thực hiện, deadline ký.
- Với thi công/PCCC/MEP: phạm vi công việc, hồ sơ thiết kế, tiêu chuẩn nghiệm thu, yêu cầu pháp lý/giấy phép/PCCC, bảo hành, bảo hiểm, an toàn lao động.
- Với lao động/giao khoán: quan hệ mong muốn là lao động hay dân sự/thương mại? Có quản lý thời giờ, địa điểm, điều hành trực tiếp, trả lương định kỳ không?

## Core legal map for Vietnam

Do not overclaim. Cite article numbers only when reasonably certain; otherwise say “cần đối chiếu điều khoản cụ thể”. Prioritize current effective law and warn that validity/freshness should be checked.

Common legal sources to consider:

- Bộ luật Dân sự 2015: giao dịch dân sự, đại diện, hợp đồng, phạt/bồi thường, bất khả kháng, đơn phương chấm dứt.
- Luật Thương mại 2005: mua bán hàng hóa, dịch vụ thương mại, phạt vi phạm thương mại, bồi thường thiệt hại, giao nhận, khiếu nại.
- Bộ luật Lao động 2019: HĐLĐ, thử việc, tiền lương, thời giờ làm việc/nghỉ ngơi, kỷ luật, chấm dứt, bảo hiểm liên quan.
- Luật Doanh nghiệp: tư cách pháp nhân, người đại diện theo pháp luật/ủy quyền, thẩm quyền ký.
- Luật Xây dựng và văn bản sửa đổi; nghị định/thông tư về hợp đồng xây dựng, quản lý chất lượng, nghiệm thu, bảo hành.
- Luật Đấu thầu nếu hợp đồng liên quan dự án/nguồn vốn phải đấu thầu.
- Luật An toàn, vệ sinh lao động; quy định bảo hộ lao động, tai nạn lao động.
- Quy định PCCC liên quan thiết kế, thẩm duyệt, nghiệm thu, trách nhiệm thi công/bảo trì khi hợp đồng có PCCC.
- Quy định thuế, hóa đơn, GTGT, TNDN, TNCN khi điều khoản thanh toán/nhân công ảnh hưởng nghĩa vụ thuế.
- Luật Trọng tài thương mại / Bộ luật Tố tụng dân sự cho giải quyết tranh chấp.

## Review workflow

1. **Ingest & normalize**
   - If file is DOCX/PDF/image, extract text first using appropriate document/OCR tools.
   - Preserve clause numbers and headings.
   - Note missing pages, unreadable scans, or attachments not provided.

2. **Classify contract**
   - Identify contract type, parties, position of the user, value, timeline, jurisdiction, governing law, dispute forum.
   - Flag if a “giao khoán/khoán việc” may actually be an employment relationship because of subordination, fixed working hours, direct management, recurring salary, tools/place controlled by employer.

3. **Business summary**
   - Summarize: purpose, scope, price/payment, schedule, deliverables, acceptance, warranty, key obligations, termination, penalties, dispute forum.

4. **Clause-by-clause risk review**
   - Rate each issue: **Đỏ / Vàng / Xanh**.
     - Đỏ: could block signing, illegal/unenforceable, major financial/operational exposure, missing critical clause.
     - Vàng: negotiable risk, ambiguity, imbalance, operational burden.
     - Xanh: acceptable or minor drafting improvement.
   - For each issue include: clause, problem, why it matters, Vietnam-law/business basis, proposed fix.

5. **Missing clause checklist**
   - Identify clauses absent or too weak for this contract type.

6. **Proposed wording / redline**
   - Provide replacement Vietnamese wording for high-impact clauses.
   - If exact redline cannot be generated, provide “Đề xuất sửa thành:” blocks.

7. **Decision recommendation**
   - End with one of:
     - Có thể ký.
     - Có thể ký sau khi sửa các điểm Vàng/Đỏ nêu dưới đây.
     - Nên yêu cầu luật sư/ban pháp chế rà soát trước khi ký.
     - Không nên ký theo bản hiện tại.

## Drafting workflow

When drafting from scratch, produce in this order:

1. Assumptions and missing information.
2. Data sheet for the user to fill: parties, tax codes, representatives, addresses, price, scope, timeline, payment, attachments.
3. Contract outline.
4. Full draft in Vietnamese with numbered clauses.
5. Checklist of attachments and signing documents.
6. Negotiation notes: points to decide before issuing to counterparty.

Prefer Vietnamese contract drafting style: clear numbered articles, defined terms, avoid vague obligations, include attachments and order of priority between contract and appendices.

## Type-specific checklists

### A. Hợp đồng lao động

Check at least:

- Party information and authority to sign.
- Job title, workplace, job description, reporting line.
- Term type and probation handling.
- Salary, allowances, payment method/date, overtime, bonuses.
- Working time, rest time, leave.
- Social insurance, health insurance, unemployment insurance obligations.
- Occupational safety, tools/assets, confidentiality.
- Training cost reimbursement if any.
- Transfer/change of job, suspension, termination, notice period.
- Non-compete clauses: flag enforceability risk; prefer confidentiality, non-solicit, IP protection instead of broad restraint.
- Personal data/privacy if collecting employee data.
- Internal labor rules, disciplinary process.

### B. Hợp đồng kinh tế / thương mại / dịch vụ / mua bán

Check at least:

- Subject matter and specifications.
- Delivery/performance location and timeline.
- Price, VAT, invoice timing, payment milestones, retention, late payment interest.
- Acceptance criteria, inspection, rejection, cure period.
- Warranties, defects, maintenance/support.
- Penalty and damages: distinguish phạt vi phạm and bồi thường; consider statutory limits in commercial contracts.
- Limitation of liability: whether acceptable for the user's position.
- Force majeure and change in law.
- Confidentiality, IP, data, subcontracting/assignment.
- Termination, suspension, consequences of termination.
- Dispute resolution, governing law, jurisdiction/arbitration.

### C. Hợp đồng thi công xây dựng / MEP / PCCC

Check at least:

- Scope boundary: supply, installation, testing/commissioning, hồ sơ hoàn công, hướng dẫn vận hành, bảo trì.
- Design documents/specifications/BOQ and order of priority.
- Site handover conditions and dependency on other contractors.
- Schedule, milestones, delay causes, extension of time, liquidated damages/penalty.
- Materials/equipment approval, CO/CQ, origin, substitutions.
- Safety, site rules, insurance, environmental obligations.
- Quality control, inspection, nghiệm thu từng phần/toàn bộ, defects list.
- Payment: advance, progress payment, retention, final settlement, VAT invoices.
- Warranty period, warranty bond/retention release.
- Change orders/variations and price adjustment.
- PCCC-specific: thẩm duyệt/thiết kế/nghiệm thu PCCC responsibilities; clarify who obtains approvals, who prepares records, and what standard applies.
- Interface risks: điện, nước, kiến trúc, HVAC, fire alarm, sprinkler, pump room, BMS, access control.
- Suspension/termination and handover of unfinished works.

### D. Hợp đồng giao khoán / khoán việc / khoán nhân công

Check at least:

- Result-based scope and deliverables; avoid language that creates employment relationship if not intended.
- Independence of contractor; tools, methods, workforce management, taxes/insurance.
- Lump sum/unit price, payment by accepted output, deductions/retention.
- Acceptance criteria and rework obligations.
- Safety, site discipline, liability for personnel, insurance.
- Tax withholding/invoices depending on contractor type.
- No unauthorized subcontracting unless approved.
- Termination and settlement for completed accepted work.
- Flag disguised employment risks when there is continuous supervision, fixed schedule, monthly salary-like payment, company-provided tools, or disciplinary control.

## Standard output: review report

Use this structure for contract review:

```markdown
# Báo cáo rà soát hợp đồng: [tên hợp đồng]

## 1. Tóm tắt nhanh
- Loại hợp đồng:
- Vị thế của Anh/công ty:
- Giá trị/thời hạn:
- Khuyến nghị ký: [Có thể ký / Ký sau khi sửa / Cần luật sư / Không nên ký]
- Top 5 rủi ro:

## 2. Giả định & tài liệu chưa có

## 3. Bảng rủi ro
| Mức | Điều/khoản | Vấn đề | Căn cứ/ý nghĩa | Đề xuất sửa |
|---|---|---|---|---|

## 4. Điều khoản thiếu hoặc cần bổ sung

## 5. Đề xuất sửa câu chữ quan trọng
### Điều [x] - [tên điều]
Hiện tại: ...
Đề xuất sửa thành: ...
Lý do: ...

## 6. Checklist trước khi ký

## 7. Câu hỏi cần làm rõ với đối tác
```

## Standard output: new draft contract

Use this structure:

```markdown
# Dự thảo [loại hợp đồng]

## A. Thông tin cần Anh xác nhận

## B. Bảng dữ liệu hợp đồng
| Trường | Nội dung |
|---|---|

## C. Dự thảo hợp đồng
[Cộng hòa xã hội...]
[Full Vietnamese contract with numbered articles]

## D. Phụ lục/hồ sơ kèm theo cần chuẩn bị

## E. Ghi chú đàm phán & rủi ro còn mở
```

## Practical rules

- Prefer precise Vietnamese wording over generic legalese.
- Separate legal risk from business risk.
- Do not fabricate legal article numbers. If uncertain, cite statute name only and recommend verification.
- For high-stakes contracts, recommend lawyer/legal department review even after AI review.
- For Thăng Long / PCCC / MEP contexts, pay special attention to nghiệm thu PCCC, hồ sơ hoàn công, trách nhiệm thẩm duyệt/nghiệm thu, bảo hành, vật tư thiết bị, tiến độ phụ thuộc mặt bằng, và thanh toán theo mốc nghiệm thu.
- When output is long, start with executive summary and risk table first; put detailed redline below.
