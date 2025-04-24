import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 设置页面配置
st.set_page_config(
    page_title="上海充电桩分布可视化",
    page_icon="⚡",
    layout="wide"
)

# 设置页面样式
st.markdown("""
    <style>
    /* 基础样式 */
    .stApp {
        background: linear-gradient(to bottom right, #0a192f, #112240) !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* 动态背景 */
    .background-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }

    /* 网格背景 */
    .grid {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background-image: 
            linear-gradient(rgba(100, 255, 218, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(100, 255, 218, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: rotate 30s linear infinite;
        opacity: 0.3;
    }

    /* 流动线条 */
    .flow-lines {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(100, 255, 218, 0.05) 10px,
            rgba(100, 255, 218, 0.05) 20px
        );
        animation: flow 15s linear infinite;
        opacity: 0.2;
    }

    /* 光点效果 */
    .glow {
        position: absolute;
        width: 150px;
        height: 150px;
        background: radial-gradient(
            circle,
            rgba(100, 255, 218, 0.15) 0%,
            transparent 70%
        );
        border-radius: 50%;
        animation: glow 8s ease-in-out infinite;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes flow {
        0% { transform: translateX(-50%) translateY(-50%); }
        100% { transform: translateX(50%) translateY(50%); }
    }

    @keyframes glow {
        0% { transform: translate(0, 0) scale(1); opacity: 0.5; }
        50% { transform: translate(50vw, 25vh) scale(1.5); opacity: 0.8; }
        100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
    }

    /* 内容样式 */
    .main-content {
        position: relative;
        z-index: 1;
        background: transparent !important;
    }

    /* 标题样式优化 */
    h1 {
        background: linear-gradient(120deg, #64ffda 0%, #00ff87 50%, #64ffda 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em !important;
        font-weight: 800 !important;
        text-align: center;
        margin: 20px 0 30px 0 !important;
        padding: 15px !important;
        text-shadow: 
            2px 2px 4px rgba(100, 255, 218, 0.2),
            -2px -2px 4px rgba(100, 255, 218, 0.2);
        position: relative;
        letter-spacing: 2px;
    }

    /* 标题装饰线 */
    h1::before, h1::after {
        content: '';
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #64ffda, transparent);
    }

    h1::before {
        top: 0;
    }

    h1::after {
        bottom: 0;
    }

    /* 子标题样式优化 */
    h3 {
        color: #ffffff !important;
        font-size: 1.8em !important;
        font-weight: 700 !important;
        margin: 15px 0 15px 0 !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        letter-spacing: 1px;
        background: linear-gradient(90deg, #64ffda, #00ff87);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 指标卡片样式优化 */
    .stMetric {
        background: rgba(13, 27, 54, 0.98) !important;
        border: 2px solid rgba(100, 255, 218, 0.5) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(100, 255, 218, 0.2) inset !important;
        border-color: rgba(100, 255, 218, 0.6) !important;
    }

    .stMetric [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 1.3em !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
    }

    .stMetric [data-testid="stMetricValue"] {
        color: #64ffda !important;
        font-size: 2.2em !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(100, 255, 218, 0.4);
    }

    .stMetric [data-testid="stMetricDelta"] {
        color: #ffffff !important;
        font-size: 1.1em !important;
        font-weight: 500 !important;
        background: rgba(100, 255, 218, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
    }

    /* 筛选区容器样式 */
    .filter-container {
        background: rgba(13, 27, 54, 0.98) !important;
        border: 1px solid rgba(100, 255, 218, 0.5) !important;
        border-radius: 8px !important;
        padding: 5px 10px !important;
        margin-bottom: 10px !important;
        box-shadow: none !important;
    }

    /* 选择器和标签样式优化 */
    .stSelectbox, .stRadio {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }

    .stSelectbox select {
        font-size: 0.9em !important;
        padding: 2px 8px !important;
        background-color: rgba(13, 27, 54, 0.98) !important;
        color: #64ffda !important;
        border: 1px solid rgba(100, 255, 218, 0.3) !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        height: 28px !important;
    }

    /* Radio按钮样式优化 */
    .stRadio > div {
        display: flex !important;
        gap: 5px !important;
        justify-content: flex-start !important;
    }

    .stRadio [role="radiogroup"] {
        padding: 0 !important;
        gap: 5px !important;
    }

    .stRadio label[data-baseweb="radio"] {
        padding: 2px 8px !important;
        border-radius: 4px !important;
        border: 1px solid rgba(100, 255, 218, 0.3) !important;
        margin: 0 !important;
    }

    .stRadio label[data-baseweb="radio"] div {
        font-size: 0.9em !important;
        font-weight: 500 !important;
        color: #64ffda !important;
    }

    /* 筛选区标题样式 */
    .filter-label {
        color: #ffffff !important;
        font-size: 0.9em !important;
        font-weight: 600 !important;
        margin: 0 !important;
        padding: 0 5px !important;
        display: inline-block !important;
    }

    /* 数据表格样式优化 */
    .stDataFrame {
        background: rgba(13, 27, 54, 0.98) !important;
        border: 2px solid rgba(100, 255, 218, 0.5) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    .stDataFrame th {
        background-color: rgba(100, 255, 218, 0.15) !important;
        color: #ffffff !important;
        font-size: 1.1em !important;
        font-weight: 700 !important;
        padding: 12px !important;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
    }

    .stDataFrame td {
        color: #64ffda !important;
        font-size: 1em !important;
        padding: 10px !important;
        font-weight: 500 !important;
    }

    /* 图表容器样式优化 */
    [data-testid="column"] {
        background: rgba(13, 27, 54, 0.98) !important;
        border: 2px solid rgba(100, 255, 218, 0.5) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin: 8px !important;
    }

    /* 地图容器样式优化 */
    #container {
        background: rgba(13, 27, 54, 0.98) !important;
        border: 2px solid rgba(100, 255, 218, 0.5) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* 信息面板样式优化 */
    #info-panel {
        background: rgba(13, 27, 54, 0.98) !important;
        border: 2px solid rgba(100, 255, 218, 0.5) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    #info-panel h3 {
        color: #ffffff !important;
        font-size: 1.6em !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    #info-content {
        color: #64ffda !important;
        font-size: 1.1em !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }

    /* 分割线样式 */
    hr {
        margin: 15px 0 !important;
        border-color: rgba(100, 255, 218, 0.3) !important;
    }

    /* 图表标题样式 */
    .js-plotly-plot .plotly .gtitle {
        font-size: 1.6em !important;
        font-weight: 700 !important;
        fill: #ffffff !important;
    }
    </style>

    <div class="background-container">
        <div class="grid"></div>
        <div class="flow-lines"></div>
        <div class="glow"></div>
        <div class="glow" style="animation-delay: -4s; left: 60%;"></div>
        <div class="glow" style="animation-delay: -2s; left: 25%; top: 50%;"></div>
    </div>
""", unsafe_allow_html=True)

# 上海各区域中心点坐标
DISTRICT_CENTERS = {
    "全上海": {"lng": 121.4737, "lat": 31.2304, "zoom": 10},
    "浦东新区": {"lng": 121.5447, "lat": 31.2224, "zoom": 11},
    "黄浦区": {"lng": 121.4846, "lat": 31.2312, "zoom": 13},
    "徐汇区": {"lng": 121.4367, "lat": 31.1889, "zoom": 13},
    "长宁区": {"lng": 121.4241, "lat": 31.2204, "zoom": 13},
    "静安区": {"lng": 121.4484, "lat": 31.2290, "zoom": 13},
    "普陀区": {"lng": 121.3952, "lat": 31.2495, "zoom": 13},
    "虹口区": {"lng": 121.4882, "lat": 31.2646, "zoom": 13},
    "杨浦区": {"lng": 121.5260, "lat": 31.2595, "zoom": 13},
    "闵行区": {"lng": 121.3810, "lat": 31.1107, "zoom": 12},
    "宝山区": {"lng": 121.4346, "lat": 31.4045, "zoom": 12},
    "嘉定区": {"lng": 121.2655, "lat": 31.3747, "zoom": 12},
    "金山区": {"lng": 121.3416, "lat": 30.7418, "zoom": 12},
    "松江区": {"lng": 121.2276, "lat": 31.0322, "zoom": 12},
    "青浦区": {"lng": 121.1241, "lat": 31.1497, "zoom": 12},
    "奉贤区": {"lng": 121.4741, "lat": 30.9179, "zoom": 12},
    "崇明区": {"lng": 121.3973, "lat": 31.6229, "zoom": 11}
}

# 读取Excel数据
@st.cache_data
def load_data():
    try:
        # 使用 pandas 直接从 GitHub raw 链接读取数据
        url = "https://raw.githubusercontent.com/zh-box/shanghai/main/data/charging_stations.csv"
        
        try:
            # 首先尝试从GitHub读取
            df = pd.read_csv(url)
        except:
            # 如果GitHub读取失败，尝试从本地读取（用于本地开发）
            df = pd.read_excel(r"C:\Users\86137\Desktop\共享充电桩\上海各区充电站信息.xlsx")
        
        # 转换数据类型
        df["充电费（元/度）"] = pd.to_numeric(df["充电费（元/度）"], errors='coerce')
        df["服务费（元/小时或度）"] = pd.to_numeric(df["服务费（元/小时或度）"], errors='coerce')
        df["快充数量"] = pd.to_numeric(df["快充数量"], errors='coerce')
        df["慢充数量"] = pd.to_numeric(df["慢充数量"], errors='coerce')
        df["经度"] = pd.to_numeric(df["经度"], errors='coerce')
        df["纬度"] = pd.to_numeric(df["纬度"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"读取数据时出错: {str(e)}")
        return None

def create_map_html(df, show_type="all", selected_district="全上海"):
    # 获取选中区域的中心点和缩放级别
    center = DISTRICT_CENTERS[selected_district]

    # 更新配色方案
    color_schemes = {
        "fast": {
            "marker": "rgba(0, 255, 255, 0.8)",  # 青色
            "circle": "rgba(0, 255, 255, 0.2)",
            "stroke": "rgba(0, 255, 255, 0.5)"
        },
        "slow": {
            "marker": "rgba(0, 255, 136, 0.8)",  # 绿色
            "circle": "rgba(0, 255, 136, 0.2)",
            "stroke": "rgba(0, 255, 136, 0.5)"
        },
        "all": {
            "marker": "rgba(255, 255, 255, 0.8)",  # 白色
            "circle": "rgba(255, 255, 255, 0.2)",
            "stroke": "rgba(255, 255, 255, 0.5)"
        }
    }

    # 生成标记点数据
    markers_data = []
    for _, row in df.iterrows():
        if show_type == "fast" and row['快充数量'] == 0:
            continue
        if show_type == "slow" and row['慢充数量'] == 0:
            continue

        scheme = color_schemes["fast" if show_type == "fast" else "slow" if show_type == "slow" else "all"]

        # 格式化数据为字符串
        info = {
            'name': str(row['地点名称']),
            'fast': str(row['快充数量']),
            'slow': str(row['慢充数量']),
            'charge': str(row['充电费（元/度）']),
            'service': str(row['服务费（元/小时或度）']),
            'payment': str(row['支付方式']),
            'address': str(row['详细地址'])
        }

        markers_data.append({
            'position': [row['经度'], row['纬度']],
            'info': info,
            'color': scheme["marker"],
            'circle_color': scheme["circle"],
            'circle_stroke': scheme["stroke"]
        })

    markers_js = str(markers_data).replace("'", '"')

    return f"""
    <div style="display: flex; gap: 15px;">
        <div id="container" style="height: 900px; flex: 4; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);">
        </div>
        <div id="info-panel" style="flex: 1.2; max-height: 900px; overflow-y: auto; padding: 20px; background: rgba(13, 27, 54, 0.98); border: 2px solid rgba(100, 255, 218, 0.5); border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);">
            <h3 style="color: #ffffff; font-size: 1.6em; font-weight: 700; margin-bottom: 15px; text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);">充电桩信息</h3>
            <div id="info-content" style="color: #64ffda;">点击地图上的标记点查看详细信息</div>
        </div>
    </div>
    <script type="text/javascript" src="https://webapi.amap.com/maps?v=2.0&key=32951a078b982e786de918188f476321&plugin=AMap.DistrictSearch,AMap.CircleEditor"></script>
    <script>
        var map = new AMap.Map('container', {{
            'zoom': {center['zoom']},
            'center': [{center['lng']}, {center['lat']}],
            'viewMode': '2D',
            'mapStyle': 'amap://styles/dark'
        }});

        var markers = [];
        var currentCircle = null;
        var infoPanel = document.getElementById('info-content');
        var markers_data = {markers_js};

        // 创建并添加标记点
        markers_data.forEach(function(marker_data) {{
            var marker = new AMap.Marker({{
                'position': marker_data.position,
                'title': marker_data.info.name,
                'clickable': true,
                'icon': new AMap.Icon({{
                    'size': new AMap.Size(6, 6),
                    'imageSize': new AMap.Size(6, 6),
                    'image': 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(`
                        <svg width="6" height="6" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="50" cy="50" r="50" fill="${{marker_data.color}}"/>
                        </svg>
                    `),
                    'anchor': new AMap.Pixel(3, 3)
                }})
            }});

            // 点击事件处理
            marker.on('click', function(e) {{
                if (currentCircle) {{
                    map.remove(currentCircle);
                }}

                var circle = new AMap.Circle({{
                    'center': marker_data.position,
                    'radius': 2000,
                    'strokeColor': marker_data.circle_stroke,
                    'strokeWeight': 2,
                    'strokeOpacity': 1,
                    'fillColor': marker_data.circle_color,
                    'fillOpacity': 1
                }});

                map.add(circle);
                currentCircle = circle;

                document.getElementById('info-content').innerHTML = `
                    <div style="background: rgba(17, 34, 64, 0.9); border-radius: 8px; padding: 15px; margin-bottom: 12px; border: 2px solid rgba(100, 255, 218, 0.5);">
                        <h4 style="color: #ffffff; margin-bottom: 12px; font-size: 1.3em; font-weight: 600; text-shadow: 0 0 8px rgba(255, 255, 255, 0.2);">${{marker_data.info.name}}</h4>
                        <div style="color: #64ffda; line-height: 1.6; font-size: 1.1em; font-weight: 500;">
                            <p style="margin: 6px 0; padding: 8px; background: rgba(13, 27, 54, 0.8); border-radius: 6px;">
                                <span style="color: #ffffff;">快充数量:</span> 
                                <span style="color: #64ffda; font-weight: 600;">${{marker_data.info.fast}}</span>
                            </p>
                            <p style="margin: 6px 0; padding: 8px; background: rgba(13, 27, 54, 0.8); border-radius: 6px;">
                                <span style="color: #ffffff;">慢充数量:</span> 
                                <span style="color: #64ffda; font-weight: 600;">${{marker_data.info.slow}}</span>
                            </p>
                            <p style="margin: 6px 0; padding: 8px; background: rgba(13, 27, 54, 0.8); border-radius: 6px;">
                                <span style="color: #ffffff;">充电费:</span> 
                                <span style="color: #64ffda; font-weight: 600;">${{marker_data.info.charge}}元/度</span>
                            </p>
                            <p style="margin: 6px 0; padding: 8px; background: rgba(13, 27, 54, 0.8); border-radius: 6px;">
                                <span style="color: #ffffff;">服务费:</span> 
                                <span style="color: #64ffda; font-weight: 600;">${{marker_data.info.service}}元</span>
                            </p>
                            <p style="margin: 6px 0; padding: 8px; background: rgba(13, 27, 54, 0.8); border-radius: 6px;">
                                <span style="color: #ffffff;">支付方式:</span> 
                                <span style="color: #64ffda; font-weight: 600;">${{marker_data.info.payment}}</span>
                            </p>
                            <p style="margin: 6px 0; padding: 8px; background: rgba(13, 27, 54, 0.8); border-radius: 6px;">
                                <span style="color: #ffffff;">地址:</span><br>
                                <span style="color: #64ffda; font-weight: 500;">${{marker_data.info.address}}</span>
                            </p>
                        </div>
                        <p style="color: #ffffff; margin-top: 12px; font-weight: 600; text-align: center; font-size: 1.1em; text-shadow: 0 0 8px rgba(255, 255, 255, 0.2);">服务半径: 2公里</p>
                    </div>
                `;
            }});

            markers.push(marker);
        }});

        // 将所有标记点添加到地图上
        map.add(markers);

        // 添加行政区划
        if ('{selected_district}' !== '全上海') {{
            var district = new AMap.DistrictSearch({{
                'subdistrict': 0,
                'extensions': 'all',
                'level': 'district'
            }});

            district.search('{selected_district}', function(status, result) {{
                if (status === 'complete' && result.districtList[0]) {{
                    var bounds = result.districtList[0].boundaries;
                    if (bounds) {{
                        var polygon = new AMap.Polygon({{
                            'path': bounds,
                            'strokeColor': '#0091ea',
                            'strokeWeight': 2,
                            'fillColor': '#1791fc',
                            'fillOpacity': 0.1
                        }});
                        map.add(polygon);
                        map.setFitView([polygon].concat(markers));
                    }}
                }}
            }});
        }}

        // 初始化信息面板
        infoPanel.innerHTML = '<p style="color: #999;">点击地图上的标记点查看详细信息</p>';
    </script>
    """

def main():
    # 包装主要内容在一个div中
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # 使用HTML来创建更复杂的标题效果
    st.markdown("""
        <h1>
            ⚡ 上海充电桩分布可视化
            <div style="font-size: 0.4em; color: #64ffda; margin-top: 10px; font-weight: 400;">
                Shanghai Charging Station Distribution Visualization
            </div>
        </h1>
    """, unsafe_allow_html=True)

    # 读取数据
    df = load_data()
    if df is None:
        return

    # 创建顶部统计指标行，使用更醒目的样式
    st.markdown('<div style="padding: 10px 0 30px 0;">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "⚡ 总快充数量",
            f"{df['快充数量'].sum():,.0f}",
            delta="实时更新",
            delta_color="off"
        )

    with col2:
        st.metric(
            "🔌 总慢充数量",
            f"{df['慢充数量'].sum():,.0f}",
            delta="实时更新",
            delta_color="off"
        )

    with col3:
        st.metric(
            "💰 平均充电费",
            f"{df['充电费（元/度）'].mean():.2f}元/度",
            delta="实时更新",
            delta_color="off"
        )

    with col4:
        st.metric(
            "💳 平均服务费",
            f"{df['服务费（元/小时或度）'].mean():.2f}元",
            delta="实时更新",
            delta_color="off"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # 创建主布局：左侧地图，右侧统计
    main_col1, main_col2 = st.columns([3, 2])

    with main_col1:
        # 地图控制面板
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        map_controls = st.container()
        with map_controls:
            col_control1, col_control2 = st.columns([1, 2])
            with col_control1:
                st.markdown('<span class="filter-label">🌏 选择区域</span>', unsafe_allow_html=True)
                selected_district = st.selectbox(
                    "选择区域",
                    list(DISTRICT_CENTERS.keys()),
                    index=0,
                    key="district_select",
                    label_visibility="collapsed"
                )
            with col_control2:
                st.markdown('<span class="filter-label">🔍 显示类型</span>', unsafe_allow_html=True)
                show_type = st.radio(
                    "选择显示类型",
                    ["全部充电桩", "仅显示快充", "仅显示慢充"],
                    horizontal=True,
                    key="show_type",
                    label_visibility="collapsed"
                )
        st.markdown('</div>', unsafe_allow_html=True)

        # 地图显示
        map_container = st.container()
        with map_container:
            if show_type == "仅显示快充":
                map_type = "fast"
            elif show_type == "仅显示慢充":
                map_type = "slow"
            else:
                map_type = "all"

            map_html = create_map_html(df, map_type, selected_district)
            components.html(map_html, height=900)

    with main_col2:
        # 支付方式统计
        st.markdown("""
            <h3 style="color: #ffffff; font-size: 2em; font-weight: 700; margin: 20px 0; text-align: center; 
            background: linear-gradient(120deg, #64ffda 0%, #00ff87 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
            💳 支付方式分布
            </h3>
        """, unsafe_allow_html=True)

        payment_counts = df["支付方式"].value_counts()
        fig_payment = px.pie(
            values=payment_counts.values,
            names=payment_counts.index,
            title="支付方式占比",
            color_discrete_sequence=['#64ffda', '#00ff87', '#4ECDC4', '#00CED1', '#40E0D0']
        )
        fig_payment.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(13, 27, 54, 0.98)",
            plot_bgcolor="rgba(13, 27, 54, 0.98)",
            title_font=dict(size=28, color="#ffffff", family="Arial Black"),
            font=dict(size=16, color="#ffffff", family="Arial"),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(13, 27, 54, 0.98)",
                bordercolor="rgba(100, 255, 218, 0.5)",
                borderwidth=2,
                font=dict(size=14, color="#ffffff"),
                title=dict(font=dict(size=16, color="#64ffda"))
            ),
            margin=dict(t=50, b=20, l=20, r=20),
            height=400
        )
        # 更新饼图文字样式
        fig_payment.update_traces(
            textfont=dict(size=16, color="#ffffff"),
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>数量: %{value}<br>占比: %{percent}<extra></extra>"
        )
        st.plotly_chart(fig_payment, use_container_width=True)

        # 各区数据统计
        st.markdown("""
            <h3 style="color: #ffffff; font-size: 2em; font-weight: 700; margin: 20px 0; text-align: center; 
            background: linear-gradient(120deg, #64ffda 0%, #00ff87 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
            🏙️ 各区充电桩数据
            </h3>
        """, unsafe_allow_html=True)

        # 计算各区统计数据
        district_stats = df.groupby('地区').agg({
            '快充数量': 'sum',
            '慢充数量': 'sum',
            '充电费（元/度）': 'mean',
            '服务费（元/小时或度）': 'mean'
        }).reset_index()

        district_stats['总充电桩数量'] = district_stats['快充数量'] + district_stats['慢充数量']
        district_stats = district_stats.sort_values('总充电桩数量', ascending=False)
        district_stats.columns = ['地区', '快充数量', '慢充数量', '平均充电费(元/度)', '平均服务费(元)', '总充电桩数量']

        # 显示各区数据表格
        st.dataframe(
            district_stats.style.format({
                '平均充电费(元/度)': '{:.2f}',
                '平均服务费(元)': '{:.2f}'
            }),
            use_container_width=True,
            height=400
        )

    # 底部图表区域
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # 各区充电桩数量柱状图
        st.markdown("""
            <h3 style="color: #ffffff; font-size: 2em; font-weight: 700; margin: 20px 0; text-align: center; 
            background: linear-gradient(120deg, #64ffda 0%, #00ff87 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
            📊 各区充电桩数量分布
            </h3>
        """, unsafe_allow_html=True)

        fig_district = px.bar(
            district_stats,
            x='地区',
            y=['快充数量', '慢充数量'],
            title='各区快充和慢充数量对比',
            barmode='group',
            labels={
                'value': '充电桩数量',
                'variable': '充电类型',
                '地区': '地区'
            },
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig_district.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(13, 27, 54, 0.98)",
            plot_bgcolor="rgba(13, 27, 54, 0.98)",
            title_font=dict(size=28, color="#ffffff", family="Arial Black"),
            font=dict(size=16, color="#ffffff", family="Arial"),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(13, 27, 54, 0.98)",
                bordercolor="rgba(100, 255, 218, 0.5)",
                borderwidth=2,
                font=dict(size=14, color="#ffffff"),
                title=dict(font=dict(size=16, color="#64ffda"))
            ),
            margin=dict(t=50, b=50, l=50, r=50),
            xaxis=dict(
                title_font=dict(size=18, color="#ffffff"),
                tickfont=dict(size=14, color="#ffffff")
            ),
            yaxis=dict(
                title_font=dict(size=18, color="#ffffff"),
                tickfont=dict(size=14, color="#ffffff")
            )
        )
        fig_district.update_traces(
            textfont=dict(size=14, color="#ffffff"),
            texttemplate='%{y}',
            textposition='outside'
        )
        st.plotly_chart(fig_district, use_container_width=True)

    with col_chart2:
        # 各区充电桩总数条形图
        st.markdown("""
            <h3 style="color: #ffffff; font-size: 2em; font-weight: 700; margin: 20px 0; text-align: center; 
            background: linear-gradient(120deg, #64ffda 0%, #00ff87 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">
            📊 各区充电桩总数排名
            </h3>
        """, unsafe_allow_html=True)

        fig_bar = px.bar(
            district_stats,
            x='总充电桩数量',
            y='地区',
            orientation='h',
            title='各区充电桩总数排名',
            labels={'地区': '地区', '总充电桩数量': '充电桩数量'},
            color='总充电桩数量',
            color_continuous_scale=['#4ECDC4', '#64ffda', '#00ff87']
        )
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(13, 27, 54, 0.98)",
            plot_bgcolor="rgba(13, 27, 54, 0.98)",
            title_font=dict(size=28, color="#ffffff", family="Arial Black"),
            font=dict(size=16, color="#ffffff", family="Arial"),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(13, 27, 54, 0.98)",
                bordercolor="rgba(100, 255, 218, 0.5)",
                borderwidth=2,
                font=dict(size=14, color="#ffffff")
            ),
            margin=dict(t=50, b=50, l=50, r=50),
            xaxis=dict(
                title_font=dict(size=18, color="#ffffff"),
                tickfont=dict(size=14, color="#ffffff")
            ),
            yaxis=dict(
                title_font=dict(size=18, color="#ffffff"),
                tickfont=dict(size=14, color="#ffffff")
            )
        )
        # 更新颜色条的配置
        fig_bar.update_coloraxes(
            colorbar=dict(
                title="充电桩数量",
                tickfont=dict(color="#ffffff", size=14),
                title_font=dict(color="#64ffda", size=16),
                len=0.8,
                thickness=20,
                bgcolor="rgba(13, 27, 54, 0.98)",
                outlinewidth=0
            )
        )
        # 添加数值标签
        fig_bar.update_traces(
            texttemplate='%{x}',
            textposition='outside',
            textfont=dict(size=14, color="#ffffff")
        )
        # 显示图表
        st.plotly_chart(fig_bar, use_container_width=True)

    # 调整页面间距
    st.markdown('<div style="padding: 2px 0 2px 0;">', unsafe_allow_html=True)

    # 调整图表布局
    st.markdown('<div style="margin: 2px 0;">', unsafe_allow_html=True)

    # 更新图表配置
    fig_payment.update_layout(
        height=450,  # 增加图表高度
        margin=dict(t=40, b=40, l=40, r=40)
    )

    fig_district.update_layout(
        height=450,  # 增加图表高度
        margin=dict(t=40, b=40, l=40, r=40)
    )

    fig_bar.update_layout(
        height=450,  # 增加图表高度
        margin=dict(t=40, b=40, l=40, r=40)
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
# cd c:\Users\86137\Desktop
# streamlit run 上海.py
