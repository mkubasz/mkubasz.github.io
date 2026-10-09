import { chromium } from "playwright";
import { PDFDocument } from "pdf-lib";
import { spawn } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import process from "node:process";

const port = 4321;
const origin = `http://127.0.0.1:${port}`;
const output = new URL("../output/pdf/Mateusz-Kubaszek-CV.pdf", import.meta.url);
const publicCopy = new URL("../public/Mateusz-Kubaszek-CV.pdf", import.meta.url);

await mkdir(new URL("../output/pdf/", import.meta.url), { recursive: true });

const server = spawn("npm", ["run", "dev", "--", "--host", "127.0.0.1", "--port", String(port)], {
  stdio: "ignore",
});

async function waitForServer() {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    try {
      const response = await fetch(`${origin}/cv`);
      if (response.ok) return;
    } catch {
      // The local server is still starting.
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error("Timed out waiting for the Astro development server.");
}

try {
  await waitForServer();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(`${origin}/cv`, { waitUntil: "networkidle" });
  await page.emulateMedia({ media: "print" });

  const pageCount = await page.locator(".cv-page").count();
  const renderedPages = [];

  for (let index = 0; index < pageCount; index += 1) {
    if (index > 0) {
      await page.goto(`${origin}/cv`, { waitUntil: "networkidle" });
      await page.emulateMedia({ media: "print" });
    }

    await page.locator(".cv-page").evaluateAll((pages, activeIndex) => {
      const selectedPage = pages[activeIndex].cloneNode(true);
      document.querySelector(".cv-document").replaceChildren(selectedPage);
    }, index);
    await page.evaluate(() => document.fonts.ready);

    renderedPages.push(
      await page.pdf({
        format: "A4",
        printBackground: true,
        preferCSSPageSize: true,
      }),
    );
  }

  const mergedDocument = await PDFDocument.create();
  for (const renderedPage of renderedPages) {
    const sourceDocument = await PDFDocument.load(renderedPage);
    const [sourcePage] = await mergedDocument.copyPages(sourceDocument, [0]);
    mergedDocument.addPage(sourcePage);
  }

  const mergedPdf = await mergedDocument.save();
  await writeFile(output, mergedPdf);
  await writeFile(publicCopy, mergedPdf);
  await browser.close();
  console.log(`Generated ${output.pathname}`);
} finally {
  server.kill("SIGTERM");
}
