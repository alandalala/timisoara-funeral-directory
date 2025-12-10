import { test, expect } from '@playwright/test';

test.describe('API Routes', () => {
  test('GET /api/companies returns companies list', async ({ request }) => {
    const response = await request.get('/api/companies');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data).toHaveProperty('data');
    expect(data).toHaveProperty('pagination');
    expect(Array.isArray(data.data)).toBeTruthy();
  });

  test('GET /api/companies with pagination', async ({ request }) => {
    const response = await request.get('/api/companies?page=1&limit=5');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.pagination.page).toBe(1);
    expect(data.pagination.limit).toBe(5);
  });

  test('GET /api/companies with county filter', async ({ request }) => {
    const response = await request.get('/api/companies?county=Timiș');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data).toHaveProperty('data');
  });

  test('GET /api/companies/[slug] returns single company', async ({ request }) => {
    const response = await request.get('/api/companies/funerare-timisoara-central');
    
    // May return 200 or 404 depending on data
    if (response.ok()) {
      const data = await response.json();
      expect(data).toHaveProperty('data');
      expect(data.data).toHaveProperty('name');
      expect(data.data).toHaveProperty('slug');
    } else {
      expect(response.status()).toBe(404);
    }
  });

  test('GET /api/companies/[slug] returns 404 for non-existent', async ({ request }) => {
    const response = await request.get('/api/companies/non-existent-slug-12345');
    
    expect(response.status()).toBe(404);
  });

  test('GET /api/counties returns counties list', async ({ request }) => {
    const response = await request.get('/api/counties');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data).toHaveProperty('data');
    expect(Array.isArray(data.data)).toBeTruthy();
  });

  test('GET /api/cities requires county parameter', async ({ request }) => {
    const response = await request.get('/api/cities');
    
    expect(response.status()).toBe(400);
  });

  test('GET /api/cities with county returns cities', async ({ request }) => {
    const response = await request.get('/api/cities?county=Timiș');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data).toHaveProperty('data');
    expect(data).toHaveProperty('county');
  });

  test('POST /api/reports requires fields', async ({ request }) => {
    const response = await request.post('/api/reports', {
      data: {},
    });
    
    expect(response.status()).toBe(400);
  });

  test('POST /api/removal-request requires fields', async ({ request }) => {
    const response = await request.post('/api/removal-request', {
      data: {},
    });
    
    expect(response.status()).toBe(400);
  });
});
