# PDF Permission Unlocker

一个本地命令行工具，用于给**已经可以正常打开**的 PDF 生成一个可编辑副本。

它适合处理这类情况：PDF 没有打开密码，但被设置了“禁止修改、禁止打印、禁止复制”等所有者权限限制。工具会重新保存一个不带这些权限限制的 PDF。

> 仅用于你拥有合法修改权或已获得授权的文件。这个工具不会破解、爆破或绕过 PDF 的打开密码。

## 功能

- 移除可打开 PDF 的所有者权限限制
- 默认不覆盖原文件，输出 `*_unlocked.pdf`
- 支持查看 PDF 状态
- Windows 下可直接使用 `unlock_pdf.cmd`

## 环境要求

- Windows、macOS 或 Linux
- Python 3.10+
- PyMuPDF

安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### Windows

把 PDF 文件拖到 `unlock_pdf.cmd` 上，或在 PowerShell 中执行：

```powershell
.\unlock_pdf.cmd "C:\path\to\input.pdf"
```

默认会在同目录生成：

```text
input_unlocked.pdf
```

指定输出路径：

```powershell
.\unlock_pdf.cmd "C:\path\to\input.pdf" -o "C:\path\to\output.pdf"
```

覆盖已存在的输出文件：

```powershell
.\unlock_pdf.cmd "C:\path\to\input.pdf" --overwrite
```

只查看 PDF 状态，不生成文件：

```powershell
.\unlock_pdf.cmd --info "C:\path\to\input.pdf"
```

### 直接使用 Python

```bash
python unlock_pdf.py "input.pdf"
python unlock_pdf.py "input.pdf" -o "output.pdf" --overwrite
python unlock_pdf.py --info "input.pdf"
```

## 输出说明

状态输出示例：

```text
pages=60, needs_pass=0, permissions=-4, encryption=None
```

- `needs_pass=0`：不需要打开密码
- `encryption=None`：输出文件不再带 PDF 加密权限限制
- 如果文件需要打开密码，工具会停止并提示无法处理

## 限制

- 不支持破解需要打开密码的 PDF
- 不保证修复损坏严重的 PDF
- 输出文件会重新保存，文件大小可能和原文件不同

