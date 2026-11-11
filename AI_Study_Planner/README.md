# AI 智慧讀書計畫助手

## 一、專題簡介
這是一個使用 Streamlit 與 OpenAI API 製作的 AI 讀書規劃工具。使用者輸入科目、學習目標、天數與每天可用時間，系統會產生結構化每日讀書計畫。

## 二、目標使用者與使用情境
- 目標使用者：需要安排讀書時間的大學生。
- 使用情境：考試前想規劃 3～14 天的複習進度。
- 解決問題：不知道每天應該讀什麼、如何分配時間。

## 三、功能
1. Streamlit 輸入欄位與按鈕。
2. 呼叫 OpenAI API 產生讀書計畫。
3. 以 Pydantic Schema 限制輸出結構（Structured Outputs）。
4. 檢查輸入空白、長度與回傳天數、時間。
5. 顯示每日任務並下載 JSON。

## 四、環境與執行方式
需要 Python 3.10 以上。

```bash
pip install -r requirements.txt
```

在 Windows PowerShell 設定 API Key（只對目前終端機有效）：

```powershell
$env:OPENAI_API_KEY="你的_API_Key"
streamlit run app.py
```

macOS / Linux：

```bash
export OPENAI_API_KEY="你的_API_Key"
streamlit run app.py
```

也可以在本機建立 `.streamlit/secrets.toml`，內容為 `OPENAI_API_KEY = "你的_API_Key"`。不要把 Key 上傳 GitHub。

## 五、資料流程
使用者輸入 → 空白與長度檢查 → OpenAI Responses API → Pydantic 結構化解析 → 檢查天數與分鐘數 → Streamlit 顯示／JSON 下載。

## 六、Prompt 設計
系統指令要求：繁體中文、務實可執行、任務天數恰好等於使用者指定天數、day 連續編號、每天分鐘數不得超過使用者可用時間。這些規則搭配程式端再次驗證。

## 七、Schema 欄位
- `title`：計畫名稱（字串）
- `goal`：學習目標（字串）
- `tips`：學習建議（字串清單）
- `tasks`：每日任務清單，每筆包含 `day`、`topic`、`minutes`、`action`

## 八、測試方式
參考 `TEST_RECORD.md`，請在設定自己的 API Key 後實際執行，填入測試結果與截圖。專題不提供虛構的測試通過紀錄。

## 九、部署方式
1. 建立 GitHub Repo，例如 `Midterm Mini-Project`，上傳程式、README 與測試紀錄。
2. 前往 Streamlit Community Cloud，連結 GitHub Repo，主檔選 `app.py`。
3. 在 Cloud 的 Secrets 設定 `OPENAI_API_KEY`，不可公開 API Key。
4. 部署後實測網站，將網址補到下方。

**GitHub Repo：** 待填

**Streamlit Cloud 網址：** 待填

## 十、限制與改善方向
- API 需要網路與有效額度，可能產生費用。
- AI 計畫不一定完全適合每個人，需自行判斷。
- 未來可增加行事曆整合、進度追蹤與學習提醒。

## 十一、作業設計說明
本專題自行選擇「AI 讀書規劃」情境，並自行設計輸入欄位、Prompt、Schema、結果畫面與驗證規則。請依自己的理解修改並補上真實測試紀錄。
