import streamlit as st
import streamlit.components.v1 as components
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

usernames = ["zhijie", "yijun", "team4", "parth", "srikanth"]

file_path = Path(__file__).parent.parent / "streamlitUserPW.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, "streamlitMain", "abcdef", cookie_expiry_days=0)

if st.session_state["authentication_status"]:
    st.title(" Unit tests for APIs")
    # HtmlFile = open("../html/pytest_report.html", 'r')
    # source_code = HtmlFile.read() 
    components.html('''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Test Report</title>
    <link href="assets/style.css" rel="stylesheet" type="text/css"/></head>
  <body onLoad="init()">
    <script>/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */


function toArray(iter) {
    if (iter === null) {
        return null;
    }
    return Array.prototype.slice.call(iter);
}

function find(selector, elem) { // eslint-disable-line no-redeclare
    if (!elem) {
        elem = document;
    }
    return elem.querySelector(selector);
}

function findAll(selector, elem) {
    if (!elem) {
        elem = document;
    }
    return toArray(elem.querySelectorAll(selector));
}

function sortColumn(elem) {
    toggleSortStates(elem);
    const colIndex = toArray(elem.parentNode.childNodes).indexOf(elem);
    let key;
    if (elem.classList.contains('result')) {
        key = keyResult;
    } else if (elem.classList.contains('links')) {
        key = keyLink;
    } else {
        key = keyAlpha;
    }
    sortTable(elem, key(colIndex));
}

function showAllExtras() { // eslint-disable-line no-unused-vars
    findAll('.col-result').forEach(showExtras);
}

function hideAllExtras() { // eslint-disable-line no-unused-vars
    findAll('.col-result').forEach(hideExtras);
}

function showExtras(colresultElem) {
    const extras = colresultElem.parentNode.nextElementSibling;
    const expandcollapse = colresultElem.firstElementChild;
    extras.classList.remove('collapsed');
    expandcollapse.classList.remove('expander');
    expandcollapse.classList.add('collapser');
}

function hideExtras(colresultElem) {
    const extras = colresultElem.parentNode.nextElementSibling;
    const expandcollapse = colresultElem.firstElementChild;
    extras.classList.add('collapsed');
    expandcollapse.classList.remove('collapser');
    expandcollapse.classList.add('expander');
}

function showFilters() {
    const filterItems = document.getElementsByClassName('filter');
    for (let i = 0; i < filterItems.length; i++)
        filterItems[i].hidden = false;
}

function addCollapse() {
    // Add links for show/hide all
    const resulttable = find('table#results-table');
    const showhideall = document.createElement('p');
    showhideall.innerHTML = '<a href="javascript:showAllExtras()">Show all details</a> / ' +
                            '<a href="javascript:hideAllExtras()">Hide all details</a>';
    resulttable.parentElement.insertBefore(showhideall, resulttable);

    // Add show/hide link to each result
    findAll('.col-result').forEach(function(elem) {
        const collapsed = getQueryParameter('collapsed') || 'Passed';
        const extras = elem.parentNode.nextElementSibling;
        const expandcollapse = document.createElement('span');
        if (extras.classList.contains('collapsed')) {
            expandcollapse.classList.add('expander');
        } else if (collapsed.includes(elem.innerHTML)) {
            extras.classList.add('collapsed');
            expandcollapse.classList.add('expander');
        } else {
            expandcollapse.classList.add('collapser');
        }
        elem.appendChild(expandcollapse);

        elem.addEventListener('click', function(event) {
            if (event.currentTarget.parentNode.nextElementSibling.classList.contains('collapsed')) {
                showExtras(event.currentTarget);
            } else {
                hideExtras(event.currentTarget);
            }
        });
    });
}

function getQueryParameter(name) {
    const match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

function init () { // eslint-disable-line no-unused-vars
    resetSortHeaders();

    addCollapse();

    showFilters();

    sortColumn(find('.initial-sort'));

    findAll('.sortable').forEach(function(elem) {
        elem.addEventListener('click',
            function() {
                sortColumn(elem);
            }, false);
    });
}

function sortTable(clicked, keyFunc) {
    const rows = findAll('.results-table-row');
    const reversed = !clicked.classList.contains('asc');
    const sortedRows = sort(rows, keyFunc, reversed);
    /* Whole table is removed here because browsers acts much slower
     * when appending existing elements.
     */
    const thead = document.getElementById('results-table-head');
    document.getElementById('results-table').remove();
    const parent = document.createElement('table');
    parent.id = 'results-table';
    parent.appendChild(thead);
    sortedRows.forEach(function(elem) {
        parent.appendChild(elem);
    });
    document.getElementsByTagName('BODY')[0].appendChild(parent);
}

function sort(items, keyFunc, reversed) {
    const sortArray = items.map(function(item, i) {
        return [keyFunc(item), i];
    });

    sortArray.sort(function(a, b) {
        const keyA = a[0];
        const keyB = b[0];

        if (keyA == keyB) return 0;

        if (reversed) {
            return keyA < keyB ? 1 : -1;
        } else {
            return keyA > keyB ? 1 : -1;
        }
    });

    return sortArray.map(function(item) {
        const index = item[1];
        return items[index];
    });
}

function keyAlpha(colIndex) {
    return function(elem) {
        return elem.childNodes[1].childNodes[colIndex].firstChild.data.toLowerCase();
    };
}

function keyLink(colIndex) {
    return function(elem) {
        const dataCell = elem.childNodes[1].childNodes[colIndex].firstChild;
        return dataCell == null ? '' : dataCell.innerText.toLowerCase();
    };
}

function keyResult(colIndex) {
    return function(elem) {
        const strings = ['Error', 'Failed', 'Rerun', 'XFailed', 'XPassed',
            'Skipped', 'Passed'];
        return strings.indexOf(elem.childNodes[1].childNodes[colIndex].firstChild.data);
    };
}

function resetSortHeaders() {
    findAll('.sort-icon').forEach(function(elem) {
        elem.parentNode.removeChild(elem);
    });
    findAll('.sortable').forEach(function(elem) {
        const icon = document.createElement('div');
        icon.className = 'sort-icon';
        icon.textContent = 'vvv';
        elem.insertBefore(icon, elem.firstChild);
        elem.classList.remove('desc', 'active');
        elem.classList.add('asc', 'inactive');
    });
}

function toggleSortStates(elem) {
    //if active, toggle between asc and desc
    if (elem.classList.contains('active')) {
        elem.classList.toggle('asc');
        elem.classList.toggle('desc');
    }

    //if inactive, reset all other functions and add ascending active
    if (elem.classList.contains('inactive')) {
        resetSortHeaders();
        elem.classList.remove('inactive');
        elem.classList.add('active');
    }
}

function isAllRowsHidden(value) {
    return value.hidden == false;
}

function filterTable(elem) { // eslint-disable-line no-unused-vars
    const outcomeAtt = 'data-test-result';
    const outcome = elem.getAttribute(outcomeAtt);
    const classOutcome = outcome + ' results-table-row';
    const outcomeRows = document.getElementsByClassName(classOutcome);

    for(let i = 0; i < outcomeRows.length; i++){
        outcomeRows[i].hidden = !elem.checked;
    }

    const rows = findAll('.results-table-row').filter(isAllRowsHidden);
    const allRowsHidden = rows.length == 0 ? true : false;
    const notFoundMessage = document.getElementById('not-found-message');
    notFoundMessage.hidden = !allRowsHidden;
}
</script>
    <h1>pytest_report.html</h1>
    <p>Report generated on 19-Aug-2022 at 14:41:57 by <a href="https://pypi.python.org/pypi/pytest-html">pytest-html</a> v3.1.1</p>
    <h2>Environment</h2>
    <table id="environment">
      <tr>
        <td>Packages</td>
        <td>{"pluggy": "1.0.0", "py": "1.11.0", "pytest": "7.1.2"}</td></tr>
      <tr>
        <td>Platform</td>
        <td>macOS-12.3.1-x86_64-i386-64bit</td></tr>
      <tr>
        <td>Plugins</td>
        <td>{"anyio": "3.6.1", "html": "3.1.1", "metadata": "2.0.2"}</td></tr>
      <tr>
        <td>Python</td>
        <td>3.9.13</td></tr></table>
    <h2>Summary</h2>
    <p>5 tests ran in 2.42 seconds. </p>
    <p class="filter" hidden="true">(Un)check the boxes to filter the results.</p><input checked="true" class="filter" data-test-result="passed" hidden="true" name="filter_checkbox" onChange="filterTable(this)" type="checkbox"/><span class="passed">5 passed</span>, <input checked="true" class="filter" data-test-result="skipped" disabled="true" hidden="true" name="filter_checkbox" onChange="filterTable(this)" type="checkbox"/><span class="skipped">0 skipped</span>, <input checked="true" class="filter" data-test-result="failed" disabled="true" hidden="true" name="filter_checkbox" onChange="filterTable(this)" type="checkbox"/><span class="failed">0 failed</span>, <input checked="true" class="filter" data-test-result="error" disabled="true" hidden="true" name="filter_checkbox" onChange="filterTable(this)" type="checkbox"/><span class="error">0 errors</span>, <input checked="true" class="filter" data-test-result="xfailed" disabled="true" hidden="true" name="filter_checkbox" onChange="filterTable(this)" type="checkbox"/><span class="xfailed">0 expected failures</span>, <input checked="true" class="filter" data-test-result="xpassed" disabled="true" hidden="true" name="filter_checkbox" onChange="filterTable(this)" type="checkbox"/><span class="xpassed">0 unexpected passes</span>
    <h2>Results</h2>
    <table id="results-table">
      <thead id="results-table-head">
        <tr>
          <th class="sortable result initial-sort" col="result">Result</th>
          <th class="sortable" col="name">Test</th>
          <th class="sortable" col="duration">Duration</th>
          <th class="sortable links" col="links">Links</th></tr>
        <tr hidden="true" id="not-found-message">
          <th colspan="4">No results found. Try to check the filters</th></tr></thead>
      <tbody class="passed results-table-row">
        <tr>
          <td class="col-result">Passed</td>
          <td class="col-name">test.py::test_past_1_week</td>
          <td class="col-duration">0.32</td>
          <td class="col-links"></td></tr>
        <tr>
          <td class="extra" colspan="4">
            <div class="log"> ------------------------------Captured stdout call------------------------------ <br/>Loaded 7 days weather!
<br/></div></td></tr></tbody>
      <tbody class="passed results-table-row">
        <tr>
          <td class="col-result">Passed</td>
          <td class="col-name">test.py::test_get_today</td>
          <td class="col-duration">0.20</td>
          <td class="col-links"></td></tr>
        <tr>
          <td class="extra" colspan="4">
            <div class="empty log">No log output captured.</div></td></tr></tbody>
      <tbody class="passed results-table-row">
        <tr>
          <td class="col-result">Passed</td>
          <td class="col-name">test.py::test_future_5_days</td>
          <td class="col-duration">0.16</td>
          <td class="col-links"></td></tr>
        <tr>
          <td class="extra" colspan="4">
            <div class="empty log">No log output captured.</div></td></tr></tbody>
      <tbody class="passed results-table-row">
        <tr>
          <td class="col-result">Passed</td>
          <td class="col-name">test.py::test_load_history_weather</td>
          <td class="col-duration">0.40</td>
          <td class="col-links"></td></tr>
        <tr>
          <td class="extra" colspan="4">
            <div class="log"> ------------------------------Captured stdout call------------------------------ <br/>Loaded history weather of 2018!
<br/></div></td></tr></tbody>
      <tbody class="passed results-table-row">
        <tr>
          <td class="col-result">Passed</td>
          <td class="col-name">test.py::test_model</td>
          <td class="col-duration">0.00</td>
          <td class="col-links"></td></tr>
        <tr>
          <td class="extra" colspan="4">
            <div class="empty log">No log output captured.</div></td></tr></tbody></table></body></html>''', height = 800)
    authenticator.logout('Logout', 'sidebar')

else:
    st.markdown('# Please go to streamlitMain login')   