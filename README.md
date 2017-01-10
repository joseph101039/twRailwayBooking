# twRailwayBooking
台鐵自動訂票程式 on Linux OS system
使用 Multiprocessing 開啟多個Chrome 瀏覽器連線至網站
用 Selenium 網頁模擬方法，以操作網頁，
並機器學習模型辨識驗證碼的部份，
先以 SVM 辨識驗證碼數字長度(5碼或6碼)，
對驗證碼圖片切割後再以 Random Forest 模型辨識數字
驗證碼辨識成功率約四成
