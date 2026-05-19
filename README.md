Để mở giao diện chính của trò chơi cờ Caro, bạn hãy chắc chắn mình đang ở trong thư mục source_code và chạy lệnh sau trên Terminal:

Bash
python main_gui.py
(Lưu ý: Trên một số hệ điều hành như macOS hoặc Ubuntu, bạn có thể cần dùng lệnh python3 main_gui.py)

Ngay sau khi chạy lệnh, cửa sổ giao diện CARO — Dark Edition sẽ xuất hiện trên màn hình.

4. Hướng Dẫn Sử Dụng Giao Diện (Gameplay Guide)
Giao diện chương trình được chia làm 3 phần chính: Bảng điểm (Bên trái), Bàn cờ (Ở giữa), và Bảng thông số kỹ thuật AI (Bên phải).

4.1. Bắt đầu một ván đấu mới
Ở bảng panel bên trái, mục "PLAY AS", bạn có thể chọn phe mình muốn chơi (Mặc định bạn là X - màu xanh, đi trước).

Nhấn nút "NEW GAME" ở bảng panel bên phải để làm mới bàn cờ và áp dụng cài đặt phe.

Click chuột vào một ô trống bất kỳ trên bàn cờ ở giữa để đánh nước đi của bạn.

AI sẽ tự động tính toán và đánh trả lại ngay sau đó. Trạng thái suy nghĩ của AI sẽ được hiển thị ở thanh Status dưới cùng.

4.2. Tính năng Hoàn tác (Undo)
Nếu bạn đi sai, bạn có thể nhấn nút "UNDO" ở bảng panel bên phải.

Chương trình sẽ lùi lại 2 bước (xóa 1 nước của AI và 1 nước của bạn), cho phép bạn đi lại từ trạng thái trước đó.

4.3. Chuyển đổi thuật toán AI
Bảng panel bên phải mục "AI MODE" cho phép bạn chọn nhanh thuật toán AI sẽ được sử dụng cho lượt đi tiếp theo của máy:

Minimax: Chạy thuật toán tìm kiếm Minimax nguyên bản (Sẽ rất chậm nếu có nhiều khoảng trống).

Alpha-Beta: Mặc định. Chạy Minimax có tích hợp cắt tỉa Alpha-Beta để tăng tốc độ.

Đối Sánh (Compare): Chạy đồng thời cả 2 thuật toán trên cùng một bàn cờ. Kết quả đối sánh (thời gian, số node duyệt) sẽ được in trực tiếp ra màn hình Terminal để so sánh hiệu năng.

4.4. Xem lại ván đấu (Review Mode)
Khi ván cờ kết thúc (Thắng, Thua, hoặc Hòa), một bảng thông báo sẽ hiện lên. Bạn có thể chọn nút "REVIEW" để xem lại tuần tự từng nước đi của cả hai bên từ đầu ván.

5. Hướng Dẫn Thay Đổi Cấu Hình Thuật Toán
Mặc định chương trình được thiết lập cấu hình Độ sâu tìm kiếm (Depth) = 3.
Nếu bạn muốn thử thách AI ở độ khó cao hơn (Depth = 4) hoặc muốn máy chạy nhanh hơn (Depth = 2), bạn cần thao tác chỉnh sửa trực tiếp trong file mã nguồn.

Mở file main_gui.py bằng bất kỳ Text Editor nào (VSCode, Notepad,...).

Tìm đến dòng số 5: ai = agent(depth=3)

Thay đổi tham số depth thành con số bạn muốn. Ví dụ:
