"""
Module 7: Interactive Web Dashboard
Provides a lightweight HTTP server serving a modern HTML5/CSS3/Chart.js
dashboard with:
- Executive Summary KPI Cards
- Interactive Risk Distribution Charts
- Student Roster Table with dynamic Search & Filtering
- Individual Student Drill-Down with Score Drivers & Recommendations
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List, Dict, Any

def generate_html_dashboard(students_json_str: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Campus Analytics | AI Student Success Platform</title>
    <!-- Chart.js & TailwindCSS via CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }}
        .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 0.75rem; }}
    </style>
</head>
<body class="p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center pb-4 border-b border-slate-700">
            <div>
                <div class="flex items-center space-x-3">
                    <span class="bg-indigo-600 text-white p-2 rounded-lg font-bold text-xl">🎓</span>
                    <h1 class="text-2xl font-bold tracking-tight text-white"> Analytics</h1>
                </div>
                <p class="text-sm text-slate-400 mt-1">AI-Powered Student Success & Early Intervention Decision Intelligence Platform</p>
            </div>
            <div class="mt-4 md:mt-0 flex items-center space-x-3">
                <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">● Real-Time AI Active</span>
                <span class="px-3 py-1 bg-slate-800 text-slate-300 rounded-lg text-xs font-medium border border-slate-700">KPMG / byteXL Challenge</span>
            </div>
        </header>

        <!-- KPI Metrics -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="kpi-cards">
            <div class="card p-5">
                <div class="text-xs uppercase text-slate-400 font-semibold">Total Monitored</div>
                <div class="text-3xl font-bold mt-2 text-white" id="stat-total">--</div>
                <div class="text-xs text-slate-400 mt-1">Across 4 Engineering Depts</div>
            </div>
            <div class="card p-5">
                <div class="text-xs uppercase text-slate-400 font-semibold">Avg Success Score</div>
                <div class="text-3xl font-bold mt-2 text-indigo-400" id="stat-avg">--</div>
                <div class="text-xs text-emerald-400 mt-1">↑ Calculated across 7 streams</div>
            </div>
            <div class="card p-5">
                <div class="text-xs uppercase text-slate-400 font-semibold">High Risk Cases</div>
                <div class="text-3xl font-bold mt-2 text-rose-500" id="stat-high-risk">--</div>
                <div class="text-xs text-rose-400 mt-1">Require immediate intervention</div>
            </div>
            <div class="card p-5">
                <div class="text-xs uppercase text-slate-400 font-semibold">Placement Ready</div>
                <div class="text-3xl font-bold mt-2 text-emerald-400" id="stat-ready">--</div>
                <div class="text-xs text-slate-400 mt-1">Coding & Aptitude &gt; 65%</div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="card p-5 lg:col-span-1">
                <h3 class="text-sm font-semibold text-slate-200 mb-4">Risk Level Distribution</h3>
                <div class="h-56"><canvas id="riskPieChart"></canvas></div>
            </div>
            <div class="card p-5 lg:col-span-2">
                <h3 class="text-sm font-semibold text-slate-200 mb-4">Student Segmentation Breakdown (Bonus)</h3>
                <div class="h-56"><canvas id="segmentBarChart"></canvas></div>
            </div>
        </div>

        <!-- Filter & Search Controls -->
        <div class="card p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
            <div class="flex items-center gap-3 w-full md:w-auto">
                <input type="text" id="searchInput" placeholder="Search student by name or ID..." 
                    class="bg-slate-900 border border-slate-700 px-4 py-2 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500 w-full md:w-72">
                <select id="filterRisk" class="bg-slate-900 border border-slate-700 px-3 py-2 rounded-lg text-sm text-slate-300">
                    <option value="ALL">All Risk Levels</option>
                    <option value="HIGH RISK">High Risk</option>
                    <option value="MEDIUM RISK">Medium Risk</option>
                    <option value="LOW RISK">Low Risk</option>
                </select>
                <select id="filterDept" class="bg-slate-900 border border-slate-700 px-3 py-2 rounded-lg text-sm text-slate-300">
                    <option value="ALL">All Departments</option>
                    <option value="Computer Science">Computer Science</option>
                    <option value="Information Tech">Information Tech</option>
                    <option value="Data Science">Data Science</option>
                    <option value="Electronics">Electronics</option>
                </select>
            </div>
            <div class="text-xs text-slate-400" id="tableRecordCount">Showing 0 students</div>
        </div>

        <!-- Student Roster Table -->
        <div class="card overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="bg-slate-800 text-xs uppercase text-slate-400 border-b border-slate-700">
                        <tr>
                            <th class="py-3 px-4">Student</th>
                            <th class="py-3 px-4">Department</th>
                            <th class="py-3 px-4">Success Score</th>
                            <th class="py-3 px-4">Academic Status</th>
                            <th class="py-3 px-4">Placement Status</th>
                            <th class="py-3 px-4">Risk Level</th>
                            <th class="py-3 px-4">AI Segment</th>
                            <th class="py-3 px-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="studentTableBody" class="divide-y divide-slate-800">
                        <!-- Rendered dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Student Detail Modal (Explainable AI & Drilldown) -->
    <div id="studentModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="card bg-slate-900 max-w-2xl w-full p-6 space-y-5 border border-slate-700 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button onclick="closeModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white text-xl font-bold">&times;</button>
            <div class="border-b border-slate-800 pb-3">
                <div class="flex items-center space-x-3">
                    <h2 class="text-xl font-bold text-white" id="modalStudentName">Student Name</h2>
                    <span id="modalRiskBadge" class="text-xs px-2.5 py-0.5 rounded-full font-bold">Risk</span>
                </div>
                <p class="text-xs text-slate-400 mt-1" id="modalStudentMeta">ID: -- | Dept: -- | Year: --</p>
            </div>

            <!-- Score Cards -->
            <div class="grid grid-cols-3 gap-3 text-center">
                <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700">
                    <div class="text-xs text-slate-400">Success Score</div>
                    <div class="text-2xl font-bold text-indigo-400" id="modalScore">--</div>
                </div>
                <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700">
                    <div class="text-xs text-slate-400">CGPA / Backlogs</div>
                    <div class="text-lg font-bold text-white" id="modalCgpa">--</div>
                </div>
                <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700">
                    <div class="text-xs text-slate-400">Attendance</div>
                    <div class="text-lg font-bold text-white" id="modalAttendance">--</div>
                </div>
            </div>

            <!-- Explainable AI Drivers -->
            <div class="space-y-3">
                <h4 class="text-xs uppercase font-semibold text-slate-300">Explainable AI: Key Score Drivers</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div class="bg-emerald-950/30 border border-emerald-800/40 p-3 rounded-lg">
                        <div class="font-semibold text-emerald-400 mb-1 flex items-center">✓ Positive Drivers</div>
                        <ul id="modalPositiveDrivers" class="space-y-1 text-slate-300 list-disc list-inside"></ul>
                    </div>
                    <div class="bg-rose-950/30 border border-rose-800/40 p-3 rounded-lg">
                        <div class="font-semibold text-rose-400 mb-1 flex items-center">⚠ Negative Drivers / Risks</div>
                        <ul id="modalNegativeDrivers" class="space-y-1 text-slate-300 list-disc list-inside"></ul>
                    </div>
                </div>
            </div>

            <!-- Prescriptive Action -->
            <div class="bg-indigo-950/40 border border-indigo-700/50 p-4 rounded-lg">
                <div class="text-xs uppercase font-semibold text-indigo-300 mb-1">Recommended Targeted Interventions</div>
                <ul id="modalInterventions" class="text-xs text-slate-200 space-y-1 list-disc list-inside"></ul>
            </div>

            <div class="flex justify-end pt-2">
                <button onclick="closeModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold">Close</button>
            </div>
        </div>
    </div>

    <script>
        const studentData = {students_json_str};

        // Initialize KPIs
        function initDashboard() {{
            document.getElementById('stat-total').innerText = studentData.length;
            const avgScore = (studentData.reduce((acc, s) => acc + s.success_score, 0) / studentData.length).toFixed(1);
            document.getElementById('stat-avg').innerText = avgScore + " / 100";
            
            const highRisks = studentData.filter(s => s.risks.overall_risk_level === 'HIGH RISK').length;
            document.getElementById('stat-high-risk').innerText = highRisks;

            const readyCount = studentData.filter(s => !s.risks.placement_risk.flag).length;
            document.getElementById('stat-ready').innerText = readyCount;

            renderCharts();
            renderTable(studentData);
        }}

        // Render Charts
        function renderCharts() {{
            // Risk Distribution
            const riskCounts = {{ 'HIGH RISK': 0, 'MEDIUM RISK': 0, 'LOW RISK': 0 }};
            studentData.forEach(s => riskCounts[s.risks.overall_risk_level]++);

            new Chart(document.getElementById('riskPieChart'), {{
                type: 'doughnut',
                data: {{
                    labels: ['High Risk', 'Medium Risk', 'Low Risk'],
                    datasets: [{{
                        data: [riskCounts['HIGH RISK'], riskCounts['MEDIUM RISK'], riskCounts['LOW RISK']],
                        backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
                        borderWidth: 0
                    }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }} }}
            }});

            // Segment Counts
            const segments = {{}};
            studentData.forEach(s => {{
                const seg = s.segmentation.segment_name;
                segments[seg] = (segments[seg] || 0) + 1;
            }});

            new Chart(document.getElementById('segmentBarChart'), {{
                type: 'bar',
                data: {{
                    labels: Object.keys(segments).map(k => k.length > 20 ? k.substring(0, 18) + '...' : k),
                    datasets: [{{
                        label: 'Students',
                        data: Object.values(segments),
                        backgroundColor: '#6366f1',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                        y: {{ ticks: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});
        }}

        // Render Student Table
        function renderTable(data) {{
            const tbody = document.getElementById('studentTableBody');
            tbody.innerHTML = '';
            document.getElementById('tableRecordCount').innerText = `Showing ${{data.length}} students`;

            data.forEach(s => {{
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/40 transition";
                
                const riskColor = s.risks.overall_risk_level === 'HIGH RISK' ? 'text-rose-400 bg-rose-500/10 border-rose-500/20' : 
                                 (s.risks.overall_risk_level === 'MEDIUM RISK' ? 'text-amber-400 bg-amber-500/10 border-amber-500/20' : 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20');

                tr.innerHTML = `
                    <td class="py-3 px-4 font-medium text-white">${{s.name}}<div class="text-xs text-slate-400">${{s.student_id}}</div></td>
                    <td class="py-3 px-4">${{s.department}}</td>
                    <td class="py-3 px-4 font-bold text-indigo-400">${{s.success_score}}</td>
                    <td class="py-3 px-4">CGPA: ${{s.raw_cgpa}} <span class="text-xs text-slate-400">(${{s.raw_backlogs}} BL)</span></td>
                    <td class="py-3 px-4">Code: ${{s.raw_coding}}%</td>
                    <td class="py-3 px-4"><span class="px-2.5 py-1 rounded-full text-xs font-semibold border ${{riskColor}}">${{s.risks.overall_risk_level}}</span></td>
                    <td class="py-3 px-4"><span class="text-xs text-slate-300 font-medium">${{s.segmentation.segment_name}}</span></td>
                    <td class="py-3 px-4 text-right">
                        <button onclick="viewStudent('${{s.student_id}}')" class="px-3 py-1 bg-indigo-600/30 hover:bg-indigo-600 border border-indigo-500/40 text-indigo-200 hover:text-white rounded text-xs transition">
                            Inspect AI
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Filter Functionality
        function applyFilters() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const risk = document.getElementById('filterRisk').value;
            const dept = document.getElementById('filterDept').value;

            const filtered = studentData.filter(s => {{
                const matchQuery = s.name.toLowerCase().includes(query) || s.student_id.toLowerCase().includes(query);
                const matchRisk = risk === 'ALL' || s.risks.overall_risk_level === risk;
                const matchDept = dept === 'ALL' || s.department === dept;
                return matchQuery && matchRisk && matchDept;
            }});

            renderTable(filtered);
        }}

        document.getElementById('searchInput').addEventListener('input', applyFilters);
        document.getElementById('filterRisk').addEventListener('change', applyFilters);
        document.getElementById('filterDept').addEventListener('change', applyFilters);

        // Modal View
        function viewStudent(id) {{
            const s = studentData.find(x => x.student_id === id);
            if (!s) return;

            document.getElementById('modalStudentName').innerText = `${{s.name}} (${{s.student_id}})`;
            document.getElementById('modalStudentMeta').innerText = `Department: ${{s.department}} | Year: ${{s.year}} | Segment: ${{s.segmentation.segment_name}}`;
            document.getElementById('modalScore').innerText = `${{s.success_score}} / 100`;
            document.getElementById('modalCgpa').innerText = `${{s.raw_cgpa}} (${{s.raw_backlogs}} Backlogs)`;
            document.getElementById('modalAttendance').innerText = `${{s.raw_attendance}}%`;

            const badge = document.getElementById('modalRiskBadge');
            badge.innerText = s.risks.overall_risk_level;
            badge.className = s.risks.overall_risk_level === 'HIGH RISK' ? 'text-xs px-2.5 py-0.5 rounded-full font-bold bg-rose-500 text-white' : 
                             (s.risks.overall_risk_level === 'MEDIUM RISK' ? 'text-xs px-2.5 py-0.5 rounded-full font-bold bg-amber-500 text-white' : 'text-xs px-2.5 py-0.5 rounded-full font-bold bg-emerald-500 text-white');

            const posList = document.getElementById('modalPositiveDrivers');
            posList.innerHTML = s.xai.top_positive_drivers.map(d => `<li>${{d}}</li>`).join('');

            const negList = document.getElementById('modalNegativeDrivers');
            negList.innerHTML = s.xai.top_negative_drivers.map(d => `<li>${{d}}</li>`).join('');

            const intList = document.getElementById('modalInterventions');
            intList.innerHTML = s.xai.recommended_interventions.map(i => `<li>${{i}}</li>`).join('');

            document.getElementById('studentModal').classList.remove('hidden');
        }}

        function closeModal() {{
            document.getElementById('studentModal').classList.add('hidden');
        }}

        window.onload = initDashboard;
    </script>
</body>
</html>"""

class CampusDashboardHandler(BaseHTTPRequestHandler):
    students_payload: str = "[]"

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html_content = generate_html_dashboard(CampusDashboardHandler.students_payload)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        elif self.path == "/api/students":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(CampusDashboardHandler.students_payload.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(processed_students: List[Dict[str, Any]], port: int = 8080):
    CampusDashboardHandler.students_payload = json.dumps(processed_students)
    server_address = ('', port)
    httpd = HTTPServer(server_address, CampusDashboardHandler)
    print(f"\n==================================================================")
    print(f"🚀 AI Student Success Dashboard is LIVE!")
    print(f"👉 Open in your web browser: http://localhost:{port}")
    print(f"==================================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()