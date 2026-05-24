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
            { label: 'Space Size',             value: c.size || '—',           section: 'capacity' },
            { label: 'Styling Stations',       value: `${c.stations || '—'} active styling chairs`, section: 'capacity' },
            { label: 'Color Bar Seats',        value: `${c.color_bar_seats || '—'} seats (for concurrent color processing)`, section: 'capacity' },
            { label: 'Total Physical Seats',   value: `${c.total_seats || '—'} seats`, section: 'capacity' },
            { label: 'Wash Basins',            value: `${c.wash_basins || 2} filtration basins`, section: 'capacity' },
            { label: 'Team Size',              value: `${c.total_staff || '—'} (${c.staff_label || '—'})`, section: 'capacity' },
            { label: 'Session Capacity',       value: c.max_capacity || '—',   section: 'capacity' },
            { label: `Operating Clients (Year 1 — ${util_y1})`, value: `${c.y1_clients || '—'} sessions/month`, section: 'capacity' },
            { label: `Operating Clients (Year 2 — ${util_y2})`, value: `${c.y2_clients || '—'} sessions/month`, section: 'capacity' },
            // Pricing
            { label: 'Average Ticket',         value: c.ticket || '—',         section: 'pricing' },
            { label: 'COGS per Session (10%)', value: c.cogs || '—',           section: 'pricing' },
            { label: 'Gross Margin per Session', value: c.margin ? `${c.ticket} × 90% = USD ${(parseInt(c.ticket.replace(/\D/g,'')) * 0.9).toFixed(2)}` : '—', section: 'pricing' },
            // Breakeven
            { label: 'Break-Even Volume (Accounting)', value: c.breakeven || '—',      section: 'breakeven' },
            { label: 'Daily Break-Even',       value: c.daily_breakeven || '—', section: 'breakeven' },
            // OPEX breakdown
            { label: 'Monthly Cash OPEX (Total)', value: c.rent_mo && c.staff_cost_mo ? 'USD ' + (c.opex_raw).toLocaleString('en-US') : '—', section: 'opex' },
            { label: '  → Rent',               value: c.rent_mo || '—',        section: 'opex', sub: true },
            { label: '  → Staff & Payroll',    value: c.staff_cost_mo || '—',  section: 'opex', sub: true },
            { label: '  → Admin, Software & Insur.', value: c.admin_sw_mo || '—', section: 'opex', sub: true },
            { label: '  → Utilities + Marketing + Misc', value: (() => {
                if (!c.opex_raw || !c.staff_cost_mo || !c.rent_mo || !c.admin_sw_raw) return '—';
                const opex = c.opex_raw;
                const rent = parseInt(c.rent_mo.replace(/\D/g,''));
                const staff = parseInt(c.staff_cost_mo.replace(/\D/g,''));
                const admin = c.admin_sw_raw;
                return 'USD ' + (opex - rent - staff - admin).toLocaleString('en-US');
            })(), section: 'opex', sub: true },
            { label: 'Monthly Non-Cash Depreciation', value: c.depreciation_mo || '—', section: 'opex' },
            { label: 'Monthly Total Accounting OPEX', value: c.total_opex_mo || '—', section: 'opex' },
            // Profit
            { label: `Monthly PAT at ${util_y2} Utilization`, value: c.y2_pat || '—', section: 'profit' },
            { label: 'PAT / Cash OPEX Ratio',  value: c.pat_ratio || '—',      section: 'profit' },
            { label: 'Corporate Tax Rate',     value: c.tax || '—',            section: 'profit' },
            // CAPEX
            { label: 'Estimated CAPEX',        value: c.capex || '—',          section: 'capex' },
            { label: '  → Biz Registration Fee', value: c.biz_reg_usd || '—',  section: 'capex', sub: true },
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
            { label: 'Fit-Out & Interior',    value: city.fitout_usd || null,  pct: `${Math.round(city.fitout_usd/capexMid*100)}%`, icon: '🏗️' },
            { label: 'Equipment & Chairs',    value: city.equip_usd || null,   pct: `${Math.round(city.equip_usd/capexMid*100)}%`, icon: '✂️' },
            { label: 'Biz Registration Fee',  value: city.biz_reg_raw || null, pct: `${Math.round(city.biz_reg_raw/capexMid*100)}%`, icon: '📄' },
            { label: 'Other Setup (Stock/PR)',value: city.other_usd || null,   pct: `${Math.round(city.other_usd/capexMid*100)}%`, icon: '📦' },
            { label: 'Lease Deposit',         value: city.deposit_usd || null, pct: `${Math.round(city.deposit_usd/capexMid*100)}%`,  icon: '🔑' },
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
            const admin = city.admin_sw_raw || 0;
            const other = opexRaw - rent - staff - admin;

            const items = [
                { label: 'Rent',                  value: rent,   icon: '🏠', color: '#e74c3c' },
                { label: 'Staff & Payroll',        value: staff,  icon: '👥', color: '#3498db' },
                { label: 'Admin & Booking SW',    value: admin,  icon: '🛡️', color: '#9b59b6' },
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

    // ── Update top KPI boxes dynamically ──────────────────────────────────────
    function populateTopKpis(city) {
        document.querySelectorAll('.stat-box').forEach(box => {
            const labelEl = box.querySelector('.label');
            const valueEl = box.querySelector('.value');
            if (!labelEl || !valueEl) return;
            const label = labelEl.textContent.trim().toLowerCase();
            if (label.includes('initial capex') || label === 'capex') {
                valueEl.textContent = city.capex || '—';
            } else if (label.includes('monthly opex') || label === 'opex') {
                valueEl.textContent = city.opex || '—';
            } else if (label.includes('breakeven volume') || label.includes('break-even')) {
                valueEl.textContent = city.daily_breakeven || '—';
            } else if (label.includes('average ticket') || label === 'ticket') {
                valueEl.textContent = city.ticket || '—';
            } else if (label.includes('setup size') || label.includes('space size')) {
                valueEl.textContent = city.size || '—';
            }
        });
    }

    // ── Update CAPEX Section Conclusion Box dynamically ───────────────────────
    function populateCapexConclusion(city) {
        const capexSection = document.querySelector('#capex, section[data-section="capex"]');
        if (!capexSection) return;
        const box = capexSection.querySelector('.conclusion-box');
        if (!box) return;

        const capexLow = city.capex_low;
        const capexHigh = city.capex_high;
        const capexMid = city.capex_mid || Math.round((capexLow + capexHigh) / 2);
        const capexStr = city.capex || 'N/A';

        box.innerHTML = `
            <strong>Total Estimate: USD ${capexMid.toLocaleString('en-US')} (Midpoint of ${capexStr} range)</strong>
        `;
    }

    // ── Update Unit Economics Post-Tax Conclusion Box dynamically ────────────
    function populatePostTaxConclusion(city) {
        const econSection = document.querySelector('#unit-economics, #economics, section[data-section="economics"]');
        if (!econSection) return;
        const box = econSection.querySelector('.conclusion-box');
        if (!box) return;

        const taxRate = city.tax_raw || 0;
        const taxPctStr = city.tax || '0%';
        const y2Pat = city.y2_pat_raw || 0;
        const preTaxProfit = taxRate < 1 ? y2Pat / (1 - taxRate) : y2Pat;
        const taxPaid = preTaxProfit * taxRate;
        const paybackStr = city.payback || '—';
        const ratioStr = city.pat_ratio || '—';

        box.innerHTML = `
            <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Post-Tax Financial Feasibility Analysis</h3>
            <p>All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of <strong>${taxPctStr}</strong>, we arrive at the following post-tax projections for the Base Case:</p>
            <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc; display: flex; flex-direction: column; gap: 0.4rem;">
                <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD ${Math.round(preTaxProfit).toLocaleString('en-US')}</li>
                <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD ${Math.round(taxPaid).toLocaleString('en-US')}</li>
                <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD ${Math.round(y2Pat).toLocaleString('en-US')}</li>
                <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>${ratioStr}</strong></li>
                <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>${paybackStr}</strong></li>
            </ul>
        `;
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

                // populateEconomicsTable(city); // Disabled to prevent conflict with script.js's 3-scenario table
                populateCapexGrid(city);
                populateOpexGrid(city);
                populateHighlights(city);
                updateMeta(city);
                populateTopKpis(city);
                populateCapexConclusion(city);
                // populatePostTaxConclusion(city); // Disabled to prevent conflict with script.js's post-tax calculations
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
