# Mitsu-SAT: theo dõi tiến bộ và phân tích câu sai SAT

## Cấu trúc
- `data/score_reports.csv`: điểm các lần thi thật (tổng, từng phần, 8 domain).
- `data/wrong_answers.csv`: mỗi dòng là một câu sai, gồm domain, kỹ năng, tiểu kỹ năng, đáp án đã
  chọn, đáp án đúng, nguyên nhân sai và ghi chú.
- `tools/analyze.py`: thống kê câu sai theo domain, kỹ năng và nguyên nhân, đối chiếu với bảng điểm,
  phát hiện lỗi lặp lại.
- `reports/`: các báo cáo phân tích.

## Chạy
```bash
python3 tools/analyze.py
python3 tools/analyze.py --since 2026-11-25   # chỉ tính các câu sai từ ngày này
```

## Mã nguyên nhân sai (`error_cause`)
| Mã | Ý nghĩa |
|---|---|
| `concept` | Hổng kiến thức / quy tắc |
| `trap` | Sa bẫy đáp án gần đúng |
| `off_goal` | Đáp án đúng sự thật nhưng không trả lời yêu cầu của đề |
| `misread` | Đọc sai / bỏ sót dữ kiện |
| `vocab` | Từ vựng / nghĩa trong ngữ cảnh |
| `careless` | Cẩu thả khi tính |
| `blank` | Bỏ trống / không kịp làm |
