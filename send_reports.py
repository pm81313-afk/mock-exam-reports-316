import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load student data
with open('students_data.json', 'r', encoding='utf-8') as f:
    students = json.load(f)

# Mapping of Seat -> Email
email_mapping = {
    "26": "310449@go.pymhs.tyc.edu.tw",
    "026": "310449@go.pymhs.tyc.edu.tw",
    # Add more seats & emails here:
    # "001": "student001@example.com",
}

def build_email_content(s):
    e1 = s['exam1']
    e2 = s['exam2']
    seat = s['seat']
    
    tot_diff = e2['total']['gp'] - e1['total']['gp']
    rank_diff = e1['total']['rank_gp_class'] - e2['total']['rank_gp_class']
    
    subject = f"【陽明高中 316 班】學測模擬考個人成績比較與衝刺指導 - 座號 {seat} 號"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; padding: 20px; }}
        .card {{ background: #ffffff; border-radius: 12px; padding: 24px; max-width: 650px; margin: 0 auto; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
        .header {{ border-bottom: 2px solid #3b82f6; padding-bottom: 12px; margin-bottom: 20px; }}
        .title {{ font-size: 20px; font-weight: bold; color: #1e3a8a; margin: 0; }}
        .subtitle {{ font-size: 13px; color: #64748b; margin-top: 4px; }}
        .highlight-box {{ background: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 6px; margin: 16px 0; font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }}
        th {{ background: #f1f5f9; color: #334155; text-align: left; padding: 8px 10px; border: 1px solid #cbd5e1; }}
        td {{ padding: 8px 10px; border: 1px solid #e2e8f0; }}
        .advice-list {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-top: 16px; }}
        .advice-item {{ margin-bottom: 10px; font-size: 13.5px; }}
        .badge-green {{ color: #166534; background: #dcfce7; padding: 2px 6px; border-radius: 4px; font-weight: bold; }}
        .badge-red {{ color: #991b1b; background: #fee2e2; padding: 2px 6px; border-radius: 4px; font-weight: bold; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <div class="title">🎓 陽明高中 316 班模擬考個人表現與進步指導</div>
          <div class="subtitle">針對第一次 (07/29) 與第二次 (09/02) 學測聯合模擬考之科目比對報告</div>
        </div>

        <p>親愛的 <strong>座號 {seat} 號</strong> 同學你好：</p>
        <p>以下為你兩次模擬考的成績變化對照與個人化備考進步建議：</p>

        <div class="highlight-box">
          <strong>📊 總級分與班級排名表現：</strong><br>
          • 第一次總級分：<strong>{e1['total']['gp']} 級分</strong> (班級排名：第 {e1['total']['rank_gp_class']} 名)<br>
          • 第二次總級分：<strong>{e2['total']['gp']} 級分</strong> (班級排名：第 {e2['total']['rank_gp_class']} 名)<br>
          • 總級分變動：<strong>{'+' if tot_diff > 0 else ''}{tot_diff} 級分</strong> ({'進步 ' + str(rank_diff) + ' 名 🏆' if rank_diff > 0 else ('持平' if rank_diff == 0 else '退步 ' + str(abs(rank_diff)) + ' 名')})
        </div>

        <h3>📋 個人科目成績比較表</h3>
        <table>
          <thead>
            <tr>
              <th>科目</th>
              <th>第一次得分 (細項)</th>
              <th>第一次級分 (班排)</th>
              <th>第二次得分 (細項)</th>
              <th>第二次級分 (班排)</th>
              <th>級分變動</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>國文</strong></td>
              <td>{e1['chinese']['score']} (國綜{e1['chinese']['choice']}+{e1['chinese']['mixed']}/寫{e1['chinese']['writing']})</td>
              <td>{e1['chinese']['gp']} 級 (第{e1['chinese']['rank']}名)</td>
              <td>{e2['chinese']['score']} (國綜{e2['chinese']['choice']}+{e2['chinese']['mixed']}/寫{e2['chinese']['writing']})</td>
              <td>{e2['chinese']['gp']} 級 (第{e2['chinese']['rank']}名)</td>
              <td>{e2['chinese']['gp'] - e1['chinese']['gp']:+d} 級</td>
            </tr>
            <tr>
              <td><strong>英文</strong></td>
              <td>{e1['english']['score']} (選{e1['english']['choice']}/手寫{e1['english']['non_choice']})</td>
              <td>{e1['english']['gp']} 級 (第{e1['english']['rank']}名)</td>
              <td>{e2['english']['score']} (選{e2['english']['choice']}/手寫{e2['english']['non_choice']})</td>
              <td>{e2['english']['gp']} 級 (第{e2['english']['rank']}名)</td>
              <td>{e2['english']['gp'] - e1['english']['gp']:+d} 級</td>
            </tr>
            <tr>
              <td><strong>數學A</strong></td>
              <td>{e1['math']['score']} (選{e1['math']['choice']}/混{e1['math']['mixed']})</td>
              <td>{e1['math']['gp']} 級 (第{e1['math']['rank']}名)</td>
              <td>{e2['math']['score']} (選{e2['math']['choice']}/混{e2['math']['mixed']})</td>
              <td>{e2['math']['gp']} 級 (第{e2['math']['rank']}名)</td>
              <td>{e2['math']['gp'] - e1['math']['gp']:+d} 級</td>
            </tr>
            <tr>
              <td><strong>社會</strong></td>
              <td>{e1['social']['score']} (選{e1['social']['choice']}/混{e1['social']['mixed']})</td>
              <td>{e1['social']['gp']} 級 (第{e1['social']['rank']}名)</td>
              <td>{e2['social']['score']} (選{e2['social']['choice']}/混{e2['social']['mixed']})</td>
              <td>{e2['social']['gp']} 級 (第{e2['social']['rank']}名)</td>
              <td>{e2['social']['gp'] - e1['social']['gp']:+d} 級</td>
            </tr>
            <tr style="background:#f8fafc; font-weight:bold;">
              <td><strong>總計</strong></td>
              <td>{e1['total']['score']} 分</td>
              <td>{e1['total']['gp']} 級 (第{e1['total']['rank_gp_class']}名)</td>
              <td>{e2['total']['score']} 分</td>
              <td>{e2['total']['gp']} 級 (第{e2['total']['rank_gp_class']}名)</td>
              <td>{tot_diff:+d} 級</td>
            </tr>
          </tbody>
        </table>

        <h3>💡 個人化讀書衝刺與進步指導建議</h3>
        <div class="advice-list">
          <div class="advice-item">📌 <strong>數學A (8級分/班排第2)：</strong>第二次數A題目難度極高，你依然穩坐全班第 2 名！選擇題 42 分基礎紮實，建議持續刷學測真題，加強觀念變體與混合題過程。</div>
          <div class="advice-item">📌 <strong>英文科 (12級分/班排第3)：</strong>選擇題勇奪 50 分高分！手寫扣分稍多，建議每週固定練習 1 篇翻譯與短文寫作，衝刺滿級分。</div>
          <div class="advice-item">📌 <strong>社會科 (11級分/班排第12)：</strong>原始分與級分同步進步（混合題得分提升至 30 分！），跨科圖表解讀能力表現優異。</div>
          <div class="advice-item">📌 <strong>國文科 (11級分/班排第22)：</strong>國綜選擇平穩，國寫部分 (22分) 為主要提升空間，建議多練習理性分析與感性題型。</div>
        </div>

        <p style="margin-top: 24px; font-size: 13px; color: #64748b; text-align: center;">預祝學測金榜題名！<br>市立陽明高中 316 班教學團隊</p>
      </div>
    </body>
    </html>
    """
    return subject, html_body

def send_email_smtp(smtp_server, smtp_port, sender_email, sender_password):
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, sender_password)
    
    for s in students:
        seat = s['seat'].lstrip('0')
        seat_padded = s['seat']
        
        target_email = email_mapping.get(seat) or email_mapping.get(seat_padded)
        if not target_email:
            print(f"Skipping Seat {seat_padded}: No email provided.")
            continue
            
        subject, html_body = build_email_content(s)
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = target_email
        
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        
        server.sendmail(sender_email, target_email, msg.as_string())
        print(f"✅ Successfully sent email to Seat {seat_padded} ({target_email})")
        
    server.quit()

if __name__ == '__main__':
    print("Email generator script ready.")
