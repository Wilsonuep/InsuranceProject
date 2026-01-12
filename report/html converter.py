import asyncio
from playwright.async_api import async_playwright
import os


async def convert_html_to_pdf(html_file, output_pdf):
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the local HTML file
        file_path = f"file://{os.path.abspath(html_file)}"
        await page.goto(file_path)

        # INJECT CSS TO PREVENT SPLITTING
        # This targets common containers like <div>, <section>, <tr>, and <p>
        # You can add specific classes here (e.g., ".notebook-cell")
        await page.add_style_tag(content="""
            div, section, tr, p, blockquote {
                break-inside: avoid;
                page-break-inside: avoid;
            }
            h1, h2, h3, h4, h5 {
                break-after: avoid;
            }
        """)

        # Emulate screen media to ensure it looks like the website
        await page.emulate_media(media="screen")

        # Generate PDF
        # 'prefer_css_page_size=True' ensures it respects the styles we just injected
        await page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"}
        )

        await browser.close()
        print(f"High-fidelity PDF created: {output_pdf}")


if __name__ == "__main__":
    # Ensure your input file exists in the same directory
    asyncio.run(convert_html_to_pdf('report/dataload.html', 'report/dudek_wilma_project_dataload.pdf'))