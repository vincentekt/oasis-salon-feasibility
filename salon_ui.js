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

                populateCapexGrid(city);
                populateOpexGrid(city);
                populateHighlights(city);
                updateMeta(city);
                populateTopKpis(city);
                populateCapexConclusion(city);
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
