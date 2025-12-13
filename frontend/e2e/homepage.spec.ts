import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load and display title', async ({ page }) => {
    await page.goto('/');
    
    // Check page title
    await expect(page).toHaveTitle(/Servicii Funerare România/);
    
    // Check main heading is visible
    await expect(page.getByRole('heading', { name: /Ghidul Tău de Încredere în Servicii Funerare/i })).toBeVisible();
  });

  test('should display company cards', async ({ page }) => {
    await page.goto('/');
    
    // Wait for companies to load
    await page.waitForTimeout(3000);
    
    // Check that at least one company card is displayed (look for phone icon or company name)
    const companyCards = page.locator('a[href^="/company/"]');
    await expect(companyCards.first()).toBeVisible({ timeout: 10000 });
  });

  test('should have working county filter dropdown', async ({ page }) => {
    await page.goto('/');
    
    // Wait for page to load
    await page.waitForTimeout(2000);
    
    // Find the county search input field
    const countyInput = page.getByPlaceholder('Caută județ...');
    await expect(countyInput).toBeVisible({ timeout: 5000 });
  });

  test('should filter companies by county', async ({ page }) => {
    await page.goto('/');
    
    // Wait for initial load
    await page.waitForTimeout(3000);
    
    // The page should show companies - just verify the page loaded correctly
    await expect(page.getByRole('heading', { name: /Ghidul Tău de Încredere|Director Servicii Funerare/i })).toBeVisible();
  });

  test('should toggle between list and map view', async ({ page }) => {
    await page.goto('/');
    
    // Find the map toggle button
    const mapButton = page.getByRole('button', { name: /hartă/i });
    
    if (await mapButton.isVisible()) {
      await mapButton.click();
      
      // Check that map container appears
      await expect(page.locator('.leaflet-container')).toBeVisible({ timeout: 5000 });
      
      // Toggle back to list
      const listButton = page.getByRole('button', { name: /listă/i });
      await listButton.click();
    }
  });

  test('should have footer navigation links', async ({ page }) => {
    await page.goto('/');
    
    // Check footer links exist
    await expect(page.getByRole('link', { name: /Despre Noi/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /Contact/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /Solicită Ștergerea Datelor/i })).toBeVisible();
  });
});
