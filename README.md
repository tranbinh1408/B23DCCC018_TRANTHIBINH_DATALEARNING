![alt text](image.png)

---

### 1. Nhập các thư viện:
```python
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
import requests
```
- `BeautifulSoup`: Được dùng để phân tích và duyệt qua nội dung HTML từ trang web.
- `psycopg2`: Một adapter PostgreSQL cho Python, giúp kết nối và tương tác với cơ sở dữ liệu PostgreSQL.
- `sql`: Một module con của `psycopg2`, giúp viết truy vấn SQL một cách an toàn hơn.
- `requests`: Thư viện này được dùng để gửi yêu cầu HTTP để lấy dữ liệu từ các trang web.

### 2. Gửi yêu cầu HTTP:
```python
url = 'https://vietnamnet.vn/lich-thi-dau-world-cup-2022-moi-nhat-658302.html'
response = requests.get(url)
```
- `url`: Địa chỉ URL của trang web mà bạn muốn lấy lịch thi đấu World Cup.
- `requests.get(url)`: Gửi một yêu cầu HTTP GET để lấy nội dung từ URL. Kết quả trả về là đối tượng `response`.

### 3. Kiểm tra trạng thái phản hồi:
```python
if response.status_code == 200:
```
- Kiểm tra mã trạng thái HTTP của phản hồi. Nếu mã trạng thái là 200, điều đó có nghĩa là yêu cầu đã thành công và trang đã được tải xuống thành công.

### 4. Phân tích nội dung trang web:
```python
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_="maincontent main-content")
```
- `BeautifulSoup(response.content, 'html.parser')`: Sử dụng BeautifulSoup để phân tích nội dung HTML đã tải xuống.
- `soup.find('div', class_="maincontent main-content")`: Tìm thẻ `<div>` có class `maincontent main-content`, đây là khu vực chứa nội dung chính của lịch thi đấu.

### 5. Tìm tất cả các bảng trong phần nội dung:
```python
    tables = div.find_all('table')
```
- `find_all('table')`: Tìm tất cả các thẻ `<table>` trong phần `<div>`. Đây là các bảng chứa dữ liệu lịch thi đấu.

### 6. Kết nối với cơ sở dữ liệu PostgreSQL:
```python
    conn = psycopg2.connect(
        dbname="datalearn",
        user="datalearn",
        password="1",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()
```
- `psycopg2.connect(...)`: Kết nối với cơ sở dữ liệu PostgreSQL bằng các thông tin cấu hình: tên cơ sở dữ liệu, tên người dùng, mật khẩu, địa chỉ máy chủ, và cổng.
- `cur = conn.cursor()`: Tạo một con trỏ để thực hiện các truy vấn SQL.

### 7. Tạo bảng nếu chưa tồn tại:
```python
    cur.execute("""
        CREATE TABLE IF NOT EXISTS world_cup (
            id SERIAL PRIMARY KEY,
            time VARCHAR(50),
            date VARCHAR(50),
            score VARCHAR(50)
        )
    """)
```
- `cur.execute(...)`: Thực thi một truy vấn SQL. Ở đây, bảng `world_cup` được tạo nếu chưa tồn tại, với các cột: `id` (khóa chính tự tăng), `time`, `date`, và `score` (tỉ số).

### 8. Duyệt qua các bảng và các hàng trong bảng:
```python
    for table in tables:
        rows = table.find_all('tr')
```
- `for table in tables`: Lặp qua từng bảng trong danh sách bảng.
- `find_all('tr')`: Tìm tất cả các thẻ `<tr>` trong mỗi bảng. Đây là các hàng dữ liệu trong bảng.

### 9. Duyệt qua các hàng và cột trong mỗi bảng:
```python
        for row in rows:
            columns = row.find_all('td')
            
            if len(columns) > 2:
                time = columns[0].text.strip()
                date = columns[1].text.strip()
                score = columns[2].text.strip()
```
- `for row in rows`: Lặp qua từng hàng trong bảng.
- `find_all('td')`: Tìm tất cả các cột (`<td>`) trong mỗi hàng.
- `if len(columns) > 2`: Kiểm tra nếu hàng có ít nhất 3 cột, để đảm bảo đây là dữ liệu hợp lệ.
- `columns[0].text.strip()`: Lấy nội dung của cột đầu tiên (thời gian), bỏ qua các khoảng trắng.
- `columns[1].text.strip()`: Lấy nội dung của cột thứ hai (ngày).
- `columns[2].text.strip()`: Lấy nội dung của cột thứ ba (tỉ số).

### 10. Chèn dữ liệu vào cơ sở dữ liệu PostgreSQL:
```python
                cur.execute(
                    sql.SQL("INSERT INTO world_cup (time, date, score) VALUES (%s, %s, %s)"),
                    [time, date, score]
                )
```
- `cur.execute(...)`: Thực thi câu lệnh SQL để chèn dữ liệu vào bảng `world_cup`. Các giá trị thời gian, ngày, và tỉ số được chèn vào tương ứng.

### 11. Cam kết thay đổi và đóng kết nối:
```python
    conn.commit()
    cur.close()
    conn.close()
```
- `conn.commit()`: Cam kết (lưu) các thay đổi vào cơ sở dữ liệu.
- `cur.close()`: Đóng con trỏ cơ sở dữ liệu.
- `conn.close()`: Đóng kết nối với cơ sở dữ liệu.

### 12. Thông báo khi hoàn thành:
```python
    print("Data has been successfully inserted into PostgreSQL database.")
```
- In ra thông báo rằng dữ liệu đã được chèn thành công vào cơ sở dữ liệu PostgreSQL.

### 13. Xử lý trường hợp thất bại:
```python
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
```
- Nếu trang web không được tải thành công, in ra mã trạng thái lỗi để thông báo về sự cố.

---

Code này của em giúp lấy lịch thi đấu World Cup từ trang web, phân tích dữ liệu, và lưu chúng vào cơ sở dữ liệu PostgreSQL.
