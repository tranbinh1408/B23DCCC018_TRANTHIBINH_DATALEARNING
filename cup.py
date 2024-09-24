from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
import requests

url = 'https://vietnamnet.vn/lich-thi-dau-world-cup-2022-moi-nhat-658302.html'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_="maincontent main-content")
    
    # Tìm tất cả các bảng trong phần `div`
    tables = div.find_all('table')
    
    # Kết nối đến PostgreSQL
    conn = psycopg2.connect(
        dbname="datalearn",
        user="datalearn",
        password="1",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()
    
    # Tạo bảng nếu chưa tồn tại
    cur.execute("""
        CREATE TABLE IF NOT EXISTS world_cup (
            id SERIAL PRIMARY KEY,
            time VARCHAR(50),
            date VARCHAR(50),
            score VARCHAR(50)
        )
    """)
    
    for table in tables:
        # Tìm tất cả các hàng trong bảng
        rows = table.find_all('tr')
        
        # Duyệt qua từng hàng
        for row in rows:
            # Tìm tất cả các cột trong mỗi hàng
            columns = row.find_all('td')
            
            if len(columns) > 2:  # Đảm bảo hàng có ít nhất 3 cột
                time = columns[0].text.strip()  # Truy cập cột đầu tiên cho thời gian
                date = columns[1].text.strip()  # Truy cập cột thứ hai cho ngày
                score = columns[2].text.strip()  # Truy cập cột thứ ba cho tỉ số
                
                # Chèn dữ liệu vào PostgreSQL
                cur.execute(
                    sql.SQL("INSERT INTO world_cup (time, date, score) VALUES (%s, %s, %s)"),
                    [time, date, score]
                )
    
    # Commit các thay đổi và đóng kết nối
    conn.commit()
    cur.close()
    conn.close()

    print("Data has been successfully inserted into PostgreSQL database.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")