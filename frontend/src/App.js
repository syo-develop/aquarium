import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement, // 追加
  LineElement, // 追加
  Tooltip,
  Legend,
  TimeScale,
} from "chart.js";
import { Line } from "react-chartjs-2";

// 必要な要素を登録
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
  Tooltip,
  Legend
);

function App() {
  // グラフデータの状態管理
  const [endpoint, setEndpoint] = useState("dayData");
  const [jsonData, setJsonData] = useState(); //初期値はDayJson

  console.log(`${endpoint}`);

  useEffect(() => {
    axios
      .get(`https://127.0.0.1:5000/api/${endpoint}`)
      .then((response) => {
        console.log("Received data:", response.data); // 取得したデータをコンソールに表示
        setJsonData(response.data); // データを状態に設定
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [endpoint]);

  useEffect(() => {
    // コンポーネントがレンダリングされた後に横スクロールを最右端に設定
    const chartWrapper = document.querySelector(".chart-wrapper");
    if (chartWrapper) {
      chartWrapper.scrollLeft = chartWrapper.scrollWidth;
    }
  }, [jsonData]);

  //読み込み中画面表示（コンポーネントしたい）
  if (!jsonData) {
    return <div>Loading...</div>;
  }

  // jsonDataが取得されてから実行する処理
  // console.log("jsonDataが取得されました:", jsonData);

  const labels = jsonData.labels.time;

  const graphData = {
    labels: labels,
    datasets: [
      {
        label: "",
        data: jsonData.datasets.temperature,
        borderColor: "rgb(75, 192, 192)",
      },
    ],
  };

  const options = {
    maintainAspectRatio: false,
    y: {
      position: "right", // 目盛を右側へ
      min: 0, // Y軸の下限
      max: 35, // Y軸の上限
    },
    plugins: {
      legend: {
        display: false, // 凡例を非表示
      },
    },
  };

  const labelCount = graphData.labels.length; // ラベルの数
  const labelWidth = 30; // ラベルの幅(px)
  const canvasWidth = labelCount * labelWidth; //グラフの横幅(px)

  return (
    <div className="App">
      <header className="header">
        <p className="header-title">水温管理</p>
      </header>
      <div className="container">
        <div className="btn-wrapper">
          <button
            className={`select-btn ${endpoint === "dayData" ? "active" : ""}`} // endpoint === DayJson時activeクラスをつける
            onClick={() => {
              setEndpoint("dayData");
            }}
          >
            日
          </button>
          <button
            className={`select-btn ${endpoint === "weekData" ? "active" : ""}`}
            onClick={() => {
              setEndpoint("weekData");
            }}
          >
            週
          </button>
          <button
            className={`select-btn ${endpoint === "monthData" ? "active" : ""}`}
            onClick={() => {
              setEndpoint("monthData");
            }}
          >
            月
          </button>
          <button
            className={`select-btn ${endpoint === "yearData" ? "active" : ""}`}
            onClick={() => {
              setEndpoint("yearData");
            }}
          >
            年
          </button>
        </div>
        <div className="chart-container">
          <p className="chart-title">{jsonData.title}</p>
          <div className="chart-wrapper">
            <div className="chart-box" style={{ width: `${canvasWidth}px` }}>
              <Line
                data={graphData}
                options={options}
                className="chart"
                id="chart-key"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
