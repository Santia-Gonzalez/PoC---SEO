const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();

        const url = 'https://omni.pro/es/';
        await page.goto(url, { waitUntil: 'networkidle2' });

        // Extraer título de la página
        const title = await page.title();

        // Extraer meta descripción
        let metaDescription;
        try {
            metaDescription = await page.$eval('meta[name="description"]', element => element.content);
        } catch (e) {
            metaDescription = 'No se encontró la meta descripción';
        }

        // Evaluar longitud del título y meta descripción
        const titleLength = title.length;
        const metaDescriptionLength = metaDescription.length;

        // Extraer todos los encabezados H1 y H2
        const h1Elements = await page.$$eval('h1', elements => elements.map(element => element.innerText));
        const h2Elements = await page.$$eval('h2', elements => elements.map(element => element.innerText));

        // Extraer todos los enlaces de la página
        const links = await page.$$eval('a', elements => elements.map(element => element.href));

        // Verificar etiquetas alt en imágenes
        const images = await page.$$eval('img', elements =>
            elements.map(element => ({
                src: element.src,
                alt: element.alt || 'Sin texto alternativo'
            }))
        );

        // Métricas de rendimiento
        const performanceMetrics = await page.evaluate(() => {
            const [navigation] = window.performance.getEntriesByType('navigation');
            return {
                domContentLoaded: navigation.domContentLoadedEventEnd,
                loadEventEnd: navigation.loadEventEnd,
                duration: navigation.duration
            };
        });

        const seoReport = {
            url: url,
            title: title,
            titleLength: titleLength,
            metaDescription: metaDescription,
            metaDescriptionLength: metaDescriptionLength,
            h1Elements: h1Elements,
            h2Elements: h2Elements,
            links: links,
            images: images,
            performanceMetrics: performanceMetrics
        };

        fs.writeFileSync('seo-report.json', JSON.stringify(seoReport, null, 2));

        console.log(`URL: ${url}`);
        console.log(`Título: ${title} (Longitud: ${titleLength})`);
        console.log(`Meta Descripción: ${metaDescription} (Longitud: ${metaDescriptionLength})`);
        console.log('Encabezados H1:', h1Elements);
        console.log('Encabezados H2:', h2Elements);
        console.log('Enlaces:', links);
        console.log('Imágenes:', images);
        console.log('Métricas de Desempeño:', performanceMetrics);


        await browser.close();
    } catch (error) {
        console.error('Error durante el análisis SEO:', error);
    }
})();
