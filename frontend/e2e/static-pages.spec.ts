import { test, expect } from '@playwright/test';

test.describe('Static Pages', () => {
  test.describe('About Page (/despre)', () => {
    test('should load about page', async ({ page }) => {
      await page.goto('/despre');
      
      await expect(page).toHaveTitle(/Despre/i);
      await expect(page.getByRole('heading', { name: /Despre Servicii Funerare România/i })).toBeVisible();
    });

    test('should display mission section', async ({ page }) => {
      await page.goto('/despre');
      
      await expect(page.getByRole('heading', { name: /Misiunea Noastră/i })).toBeVisible();
    });

    test('should have back link', async ({ page }) => {
      await page.goto('/despre');
      
      const backLink = page.getByRole('link', { name: /Înapoi la căutare/i });
      await expect(backLink).toBeVisible();
    });
  });

  test.describe('Contact Page (/contact)', () => {
    test('should load contact page', async ({ page }) => {
      await page.goto('/contact');
      
      await expect(page).toHaveTitle(/Contact/i);
      await expect(page.getByRole('heading', { name: /Contact/i })).toBeVisible();
    });

    test('should have contact form', async ({ page }) => {
      await page.goto('/contact');
      
      // Check form fields exist
      await expect(page.getByLabel(/Nume/i)).toBeVisible();
      await expect(page.getByLabel(/Email/i)).toBeVisible();
      await expect(page.getByLabel(/Subiect/i)).toBeVisible();
      await expect(page.getByLabel(/Mesaj/i)).toBeVisible();
    });

    test('should validate required fields', async ({ page }) => {
      await page.goto('/contact');
      
      // Try to submit empty form
      const submitButton = page.getByRole('button', { name: /Trimite/i });
      await submitButton.click();
      
      // Form should not submit (HTML5 validation)
      await expect(page).toHaveURL('/contact');
    });

    test('should submit form successfully', async ({ page }) => {
      await page.goto('/contact');
      
      // Fill out the form
      await page.getByLabel(/Nume/i).fill('Test User');
      await page.getByLabel(/Email/i).fill('test@example.com');
      await page.getByLabel(/Subiect/i).selectOption('general');
      await page.getByLabel(/Mesaj/i).fill('This is a test message from Playwright.');
      
      // Submit
      await page.getByRole('button', { name: /Trimite/i }).click();
      
      // Check success message appears
      await expect(page.getByRole('heading', { name: /Mesaj Trimis/i })).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('GDPR Removal Page (/eliminare)', () => {
    test('should load removal request page', async ({ page }) => {
      await page.goto('/eliminare');
      
      await expect(page).toHaveTitle(/Eliminare|GDPR/i);
      await expect(page.getByRole('heading', { name: /Solicitare Eliminare/i })).toBeVisible();
    });

    test('should display GDPR info box', async ({ page }) => {
      await page.goto('/eliminare');
      
      await expect(page.getByRole('heading', { name: /Drepturile dvs/i })).toBeVisible();
    });

    test('should have removal request form', async ({ page }) => {
      await page.goto('/eliminare');
      
      // Check form fields exist
      await expect(page.getByLabel(/Denumirea Firmei/i)).toBeVisible();
      await expect(page.getByLabel(/Nume și Prenume/i)).toBeVisible();
      await expect(page.getByLabel(/Email/i)).toBeVisible();
      await expect(page.getByLabel(/Relația cu firma/i)).toBeVisible();
      await expect(page.getByLabel(/Motivul/i)).toBeVisible();
    });
  });
});
