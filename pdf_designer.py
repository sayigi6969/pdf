import streamlit as st
from reportlab.pdfgen import canvas
import tempfile
import os

st.set_page_config(layout="wide")
st.title("📄 PDF 可视化生成器（网页版 Streamlit）")

if "elements" not in st.session_state:
    st.session_state.elements = []

with st.sidebar:
    st.header("➕ 添加元素")
    element_type = st.selectbox("元素类型", ["文本", "图片"])

    if element_type == "文本":
        text = st.text_input("文本内容", "Hello PDF")
        x = st.number_input("X 坐标", 0, 1000, 100)
        y = st.number_input("Y 坐标", 0, 1000, 750)
        size = st.number_input("字体大小", 6, 72, 20)
        if st.button("添加文本"):
            st.session_state.elements.append({
                "type": "text",
                "text": text,
                "x": x,
                "y": y,
                "size": size
            })

    elif element_type == "图片":
        image_file = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
        x = st.number_input("X 坐标", 0, 1000, 100, key="img_x")
        y = st.number_input("Y 坐标", 0, 1000, 700, key="img_y")
        width = st.number_input("宽度", 10, 1000, 100, key="img_w")
        height = st.number_input("高度", 10, 1000, 100, key="img_h")
        if image_file and st.button("添加图片"):
            img_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            img_temp.write(image_file.read())
            img_path = img_temp.name
            st.session_state.elements.append({
                "type": "image",
                "path": img_path,
                "x": x,
                "y": y,
                "width": width,
                "height": height
            })

st.subheader("🧾 当前元素列表")
for i, el in enumerate(st.session_state.elements):
    st.write(f"{i+1}. {el}")

st.subheader("🧠 自动生成的 Python3 代码")
code_lines = [
    "from reportlab.pdfgen import canvas",
    "c = canvas.Canvas('output.pdf')"
]

for el in st.session_state.elements:
    if el["type"] == "text":
        code_lines.append(f'c.setFont("Helvetica", {el["size"]})')
        code_lines.append(f'c.drawString({el["x"]}, {el["y"]}, "{el["text"]}")')
    elif el["type"] == "image":
        code_lines.append(f'c.drawImage(\"{el['path']}\", {el['x']}, {el['y']}, width={el['width']}, height={el['height']})')

code_lines.append("c.save()")
final_code = "\n".join(code_lines)
st.code(final_code, language="python")

if st.button("📤 生成 PDF 文件"):
    pdf_path = os.path.join(tempfile.gettempdir(), "output.pdf")
    c = canvas.Canvas(pdf_path)
    for el in st.session_state.elements:
        if el["type"] == "text":
            c.setFont("Helvetica", el["size"])
            c.drawString(el["x"], el["y"], el["text"])
        elif el["type"] == "image":
            c.drawImage(el["path"], el["x"], el["y"], width=el["width"], height=el["height"])
    c.save()

    with open(pdf_path, "rb") as f:
        st.download_button("📥 下载生成的 PDF", f, file_name="output.pdf", mime="application/pdf")
