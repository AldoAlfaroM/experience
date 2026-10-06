"""Contenido del CV. Edita este archivo para actualizar la landing page."""

CV = {
    "name": "Aldo Emanuel Alfaro Moreno",
    "short_name": "Aldo Alfaro",
    "title": "Software Engineer",
    "location": "Tijuana, México",
    "linkedin": "https://www.linkedin.com/in/aldo-alfaro",
    "summary": (
        "More than 5 years of experience as a software engineer. Implemented solutions "
        "in 3 web pages that helped break sales records year after year at Dragon Trade. "
        "At Swarco McCain, mostly front-end work: user-focused reports to view data and "
        "features that improved clients' experience with the app."
    ),
    "stats": [
        {"value": "5+", "label": "years building software"},
        {"value": "3", "label": "web pages behind record sales"},
        {"value": "2", "label": "companies, remote & on-site"},
    ],
    "skills": {
        "Frontend": ["TypeScript", "JavaScript", "Angular 17", "Angular Material",
                     "PrimeNG", "DevExpress", "Highcharts", "HTML", "SCSS", "UI/UX"],
        "Backend & Data": [".NET Core", "C#", "Dapper", "Minimal API","SQL Server", "MongoDB"],
        "Tools & Process": ["Git", "SourceTree", "Jira", "Confluence", "Agile", "Kanban", "Claude AI", "Postman"],
    },
    "experience": [
        {
            "company": "Swarco McCain",
            "role": "Software Engineer",
            "mode": "Remote",
            "period": "Oct 2022 – Jan 2026",
            "points": [
                "Part of the migration of a legacy .NET desktop project to an Angular web app.",
                "Refactored project modules to follow best practices and scale.",
                "Built reports with Highcharts graphs, traffic data and Angular tables, "
                "plus an exporter to PDF and Excel.",
                "Implemented CSS animations.",
                "Complex user interactions: a menu that opens a modal with dynamic tabs, "
                "tables with editable dropdown cells and saved configurations.",
                "Full-stack development on the file handler and several modules.",
                "Maintained legacy .NET microservices.",
                "Worked closely with backend engineers and product owners on "
                "client-driven development; troubleshot bugs across the whole app.",
            ],
        },
        {
            "company": "Dragon Trade",
            "role": "Software Developer",
            "mode": "On-site",
            "period": "Jan 2019 – Oct 2022",
            "points": [
                "Built a landing page with Angular and an invoice manager in the CRM.",
                "Parsers for BBVA bank statements and scanned product serial numbers, "
                "reading .txt/Excel files into Angular system reports.",
                "WMS business rules, jsReport, user management and SMTP DBMail.",
                "Improved UI/UX of the customer web page: date-based marketing carousel, "
                "featured promo slider and bug fixes.",
                "Gathered requirements directly with clients and implemented solutions.",
                "Handled files from IIS to the customer web page.",
                "Built a workplace climate survey in Angular with results in SQL Server.",
                "Shared front-line IT support duties.",
            ],
        },
    ],
    "education": [
        {
            "school": "Instituto Tecnológico de Tijuana",
            "degree": "Computer Systems Engineering",
            "period": "Jan 2015 – Jun 2020",
        }
    ],
}
