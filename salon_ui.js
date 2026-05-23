/**
 * salon_ui.js
 * ===========
 * Shared script loaded by all 27 city subpages.
 * Reads city_data.json and populates every financial section dynamically.
 *
 * Usage: each subpage must have:
 *   <body data-city="Ho Chi Minh"> (or exact city name from city_data.json)
 *   <script src="salon_ui.js"></script>
 *
 * The script auto-detects the city from data-city, fetches city_data.json,
 * and populates:
 *   - #unit-economics tbody
 *   - .capex-grid (CAPEX breakdown cards)
 *   - .opex-grid  (OPEX breakdown cards)
 *   - .staff-summary (team size summary)
 *   - .financial-highlights (hero KPI cards)
 */

(function () {
    'use strict';

    // ── Cache city data after first fetch ────────────────────────────────────
    let _cityDataCache = null;

    function fetchCityData() {
        if (_cityDataCache) return Promise.resolve(_cityDataCache);
        // Try relative path first, then absolute root
        return fetch('city_data.json')
            .catch(() => fetch('/city_data.json'))
            .then(r => r.json())
            .then(data => {
                _cityDataCache = data;
                return data;
            });
    }

    // ── Find city record by name ──────────────────────────────────────────────
    function findCity(data, name) {
        if (!name) return null;
        const n = name.toLowerCase().trim();
        return data.find(c =>
            c.name.toLowerCase() === n ||
            c.url === n + '.html'
        ) || null;
    }

    // ── Format helpers ────────────────────────────────────────────────────────
    function fmtUSD(v, decimals = 0) {
        if (v === undefined || v === null) return '—';
        return 'USD ' + Number(v).toLocaleString('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }
    function fmtPct(v) { return Number(v * 100).toFixed(1) + '%'; }

    // ── Build unit economics table rows ───────────────────────────────────────
    function buildEconomicsRows(city) {
        const c = city;
        const util_y1 = c.util_y1 || '65%';
        const util_y2 = c.util_y2 || '75%';

        const rows = [
            // Space & Capacity
            { label: 'Space',                  value: c.size || '—',           section: 'capacity' },
            { label: 'Styling Stations',       value: `${c.stations || '—'} stations + ${c.wash_basins || 2} wash basins`, section: 'capacity' },
            { label: 'Team Size',              value: `${c.total_staff || '—'} (${c.staff_label || '—'})`, section: 'capacity' },
            { label: 'Session Capacity',       value: c.max_capacity || '—',   section: 'capacity' },
            { label: `Operating Clients (Year 1 — ${util_y1})`, value: `${c.y1_clients || '—'} clients/month`, section: 'capacity' },
            { label: `Operating Clients (Year 2 — ${util_y2})`, value: `${c.y2_clients || '—'} clients/month`, section: 'capacity' },
            // Pricing
            { label: 'Average Ticket',         value: c.ticket || '—',         section: 'pricing' },
            { label: 'COGS per Session (10%)', value: c.cogs || '—',           section: 'pricing' },
            { label: 'Gross Margin per Session', value: c.margin ? `${c.ticket} × 90% = ${c.cogs ? 'USD ' + (parseInt(c.ticket.replace(/\D/g,'')) * 0.9).toFixed(2) : '—'}` : '—', section: 'pricing' },
            // Breakeven
            { label: 'Break-Even Volume',      value: c.breakeven || '—',      section: 'breakeven' },
            { label: 'Daily Break-Even',       value: c.daily_breakeven || '—', section: 'breakeven' },
            // OPEX breakdown
            { label: 'Monthly OPEX (Total)',   value: c.opex || '—',           section: 'opex' },
            { label: '  → Rent',               value: c.rent_mo || '—',        section: 'opex', sub: true },
            { label: '  → Staff & Payroll',    value: c.staff_cost_mo || '—',  section: 'opex', sub: true },
            { label: '  → Utilities + Marketing + Misc', value: (() => {
                if (!c.opex_raw || !c.staff_cost_mo || !c.rent_mo) return '—';
                const opex = c.opex_raw;
                const rent = parseInt(c.rent_mo.replace(/\D/g,''));
                const staff = parseInt(c.staff_cost_mo.replace(/\D/g,''));
                return 'USD ' + (opex - rent - staff).toLocaleString('en-US');
            })(), section: 'opex', sub: true },
            // Profit
            { label: `Monthly PAT at ${util_y2} Utilization (After Tax)`, value: c.y2_pat || '—', section: 'profit' },
            { label: 'PAT / OPEX Ratio',       value: c.pat_ratio || '—',      section: 'profit' },
            { label: 'Corporate Tax Rate',     value: c.tax || '—',            section: 'profit' },
            // CAPEX
            { label: 'Estimated CAPEX',        value: c.capex || '—',          section: 'capex' },
            { label: 'Payback Period',         value: c.payback || '—',        section: 'capex' },
        ];
        return rows;
    }

    // ── Populate #unit-economics table ────────────────────────────────────────
    function populateEconomicsTable(city) {
        const section = document.querySelector('#unit-economics, #economics, section[data-section="economics"]');
        if (!section) return;
        let tbody = section.querySelector('tbody');
        if (!tbody) return;

        const rows = buildEconomicsRows(city);
        tbody.innerHTML = rows.map(row => {
            const cls = row.sub ? ' class="sub-row"' : '';
            return `<tr${cls}>
                <td>${row.label}</td>
                <td><strong>${row.value}</strong></td>
            </tr>`;
        }).join('\n');
    }

    // ── Populate CAPEX breakdown grid ─────────────────────────────────────────
    function populateCapexGrid(city) {
        // Each subpage may have a .capex-grid or #capex-breakdown
        const grids = document.querySelectorAll('.capex-grid, #capex-breakdown, [data-section="capex-grid"]');
        if (!grids.length) return;

        const capexLow  = city.capex_low;
        const capexHigh = city.capex_high;
        const capexMid  = city.capex_mid || Math.round((capexLow + capexHigh) / 2);

        // CAPEX items derived from city_data.json fields set in excel_to_json.py
        const items = [
            { label: 'Fit-Out & Interior',    value: city.fitout_usd || null,  pct: '~52%', icon: '🏗️' },
            { label: 'Equipment & Chairs',    value: city.equip_usd || null,   pct: '~25%', icon: '✂️' },
            { label: 'Other (Legal/Stock)',   value: city.other_usd || null,   pct: '~15%', icon: '📦' },
            { label: 'Lease Deposit',         value: city.deposit_usd || null, pct: '~8%',  icon: '🔑' },
        ];

        grids.forEach(grid => {
            // Only update if it has data-auto="true" or is empty
            if (grid.dataset.auto === 'false') return;
            grid.innerHTML = `
                <div class="capex-summary">
                    <div class="capex-range">${city.capex || 'N/A'}</div>
                    <div class="capex-label">Total Estimated CAPEX</div>
                    <div class="capex-midpoint">Midpoint: USD ${capexMid.toLocaleString('en-US')}</div>
                </div>
                ${items.filter(i => i.value).map(i => `
                <div class="capex-card">
                    <div class="capex-card-icon">${i.icon}</div>
                    <div class="capex-card-label">${i.label}</div>
                    <div class="capex-card-value">USD ${Number(i.value).toLocaleString('en-US')}</div>
                    <div class="capex-card-pct">${i.pct} of total</div>
                </div>`).join('')}
            `;
        });
    }

    // ── Populate OPEX breakdown grid ──────────────────────────────────────────
    function populateOpexGrid(city) {
        const grids = document.querySelectorAll('.opex-grid, #opex-breakdown, [data-section="opex-grid"]');
        if (!grids.length) return;

        grids.forEach(grid => {
            if (grid.dataset.auto === 'false') return;

            const opexRaw = city.opex_raw || 0;
            const rent  = city.rent_mo  ? parseInt(city.rent_mo.replace(/\D/g,''))  : 0;
            const staff = city.staff_cost_mo ? parseInt(city.staff_cost_mo.replace(/\D/g,'')) : 0;
            const other = opexRaw - rent - staff;

            const items = [
                { label: 'Rent',                  value: rent,   icon: '🏠', color: '#e74c3c' },
                { label: 'Staff & Payroll',        value: staff,  icon: '👥', color: '#3498db' },
                { label: 'Utilities + Mktg + Misc',value: other,  icon: '💡', color: '#2ecc71' },
            ];

            grid.innerHTML = `
                <div class="opex-total">
                    <span class="opex-total-label">Monthly OPEX</span>
                    <span class="opex-total-value">${city.opex || 'N/A'}</span>
                </div>
                ${items.map(i => `
                <div class="opex-card" style="border-left: 4px solid ${i.color}">
                    <div class="opex-card-icon">${i.icon}</div>
                    <div class="opex-card-label">${i.label}</div>
                    <div class="opex-card-value">USD ${i.value.toLocaleString('en-US')}</div>
                    <div class="opex-card-pct">${opexRaw ? (i.value/opexRaw*100).toFixed(0) : '—'}% of OPEX</div>
                </div>`).join('')}
            `;
        });
    }

    // ── Populate financial highlight cards ────────────────────────────────────
    function populateHighlights(city) {
        // Update any element with data-field="..." to the matching city_data.json field
        document.querySelectorAll('[data-field]').forEach(el => {
            const field = el.dataset.field;
            if (city[field] !== undefined) {
                el.textContent = city[field];
            }
        });

        // Update any [data-kpi] cards (the hero stats at top of subpages)
        const kpiMap = {
            'capex':     city.capex,
            'opex':      city.opex,
            'ticket':    city.ticket,
            'payback':   city.payback,
            'pat':       city.pat_ratio,
            'breakeven': city.breakeven,
            'stations':  city.stations !== undefined ? `${city.stations} Stations` : undefined,
            'staff':     city.total_staff !== undefined ? `${city.total_staff} Staff` : undefined,
            'capacity':  city.max_capacity,
        };
        document.querySelectorAll('[data-kpi]').forEach(el => {
            const key = el.dataset.kpi;
            if (kpiMap[key] !== undefined) {
                el.textContent = kpiMap[key];
            }
        });
    }

    // ── Update page meta (breadcrumb, title badge) ────────────────────────────
    function updateMeta(city) {
        // Update any .city-format-badge elements
        document.querySelectorAll('.city-format-badge, .format-badge, [data-field="format"]').forEach(el => {
            el.textContent = city.format || '';
        });
        // Update risk note
        document.querySelectorAll('.risk-note, [data-field="risk"]').forEach(el => {
            el.textContent = city.risk || '';
        });
    }

    // ── Main init ─────────────────────────────────────────────────────────────
    function init() {
        const cityName = document.body.dataset.city;
        if (!cityName) return;  // Not a city subpage

        fetchCityData()
            .then(data => {
                const city = findCity(data, cityName);
                if (!city) {
                    console.warn(`[salon_ui] City not found: "${cityName}"`);
                    return;
                }
                console.log(`[salon_ui] Loaded: ${city.name}`);

                populateEconomicsTable(city);
                populateCapexGrid(city);
                populateOpexGrid(city);
                populateHighlights(city);
                updateMeta(city);
            })
            .catch(err => {
                console.error('[salon_ui] Failed to load city_data.json:', err);
            });
    }

    // ── Run on DOM ready ──────────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ── Expose helper for dashboard (script.js can call this too) ─────────────
    window.SalonUI = {
        fetchCityData,
        findCity,
        fmtUSD,
    };
})();
