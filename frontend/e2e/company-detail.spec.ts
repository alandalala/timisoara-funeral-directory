import { test, expect } from '@playwright/test';

test.describe('Company Detail Page', () => {
  test('should navigate to company detail from card', async ({ page }) => {
    await page.goto('/');
    
    // Wait for companies to load
    await page.waitForTimeout(2000);
    
    // Click on the first company card link
    const firstCompanyLink = page.locator('a[href^="/company/"]').first();
    await expect(firstCompanyLink).toBeVisible({ timeout: 10000 });
    
    // Get the href to verify navigation
    const href = await firstCompanyLink.getAttribute('href');
    await firstCompanyLink.click();
    
    // Verify we're on the company detail page
    await expect(page).toHaveURL(new RegExp(href || '/company/'));
  });

  test('should display company information', async ({ page }) => {
    // Go directly to a known company page
    await page.goto('/company/funerare-timisoara-central');
    
    // Wait for page to load
    await page.waitForTimeout(3000);
    
    // Check that main elements are visible - look for any h1 heading
    const heading = page.locator('h1').first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Check for any contact-related content
    const contactSection = page.locator('text=/Contact|Telefon|Email/i').first();
    await expect(contactSection).toBeVisible({ timeout: 5000 });
  });

  test('should have back to search link', async ({ page }) => {
    await page.goto('/company/funerare-timisoara-central');
    
    // Check for back link
    const backLink = page.getByRole('link', { name: /Înapoi la căutare/i });
    await expect(backLink).toBeVisible();
    
    // Click and verify navigation
    await backLink.click();
    await expect(page).toHaveURL('/');
  });

  test('should display map on company detail page', async ({ page }) => {
    await page.goto('/company/funerare-timisoara-central');
    
    // Wait for map to load
    await page.waitForTimeout(3000);
    
    // Check for map container (Leaflet)
    const mapContainer = page.locator('.leaflet-container');
    await expect(mapContainer).toBeVisible({ timeout: 10000 });
  });

  test('should show 404 for non-existent company', async ({ page }) => {
    await page.goto('/company/non-existent-company-slug-12345');
    
    // Wait for page to load
    await page.waitForTimeout(2000);
    
    // Check for not found message
    await expect(page.getByText(/Firmă Negăsită|nu a fost găsită/i)).toBeVisible();
  });
});
