import site from '../data/site.json';
import documents from '../data/documents.json';
import people from '../data/people.json';
import grantees from '../data/grantees.json';
import steps from '../data/steps.json';
import faqs from '../data/faqs.json';
import reports from '../data/reports.json';
import news from '../data/news.json';

/** Replace {{docKey}} tokens in HTML strings with the document's download path. */
export function withDocs(html) {
  return html.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    if (!documents[key]) throw new Error(`Unknown document token: ${key}`);
    return documents[key].path;
  });
}

export const nav = [
  { label: 'About the Foundation', href: '/about-the-foundation/', key: 'about', children: [
    { label: 'From the Board Chair', href: '/about-the-foundation/from-the-board-chair/' },
    { label: 'Our History', href: '/about-the-foundation/our-history/' },
    { label: 'Our Approach', href: '/about-the-foundation/our-approach/' },
    { label: 'Our People', href: '/about-the-foundation/our-people/' },
    { label: 'Financials', href: '/about-the-foundation/financials/' },
    { label: 'Annual Reports', href: '/annual-reports/' },
    { label: 'Careers', href: '/about-the-foundation/careers/' },
  ] },
  { label: 'What We Fund', href: '/what-we-fund/', key: 'fund', children: [
    { label: 'Mission & Guidelines', href: '/what-we-fund/mission-guidelines/' },
    { label: 'Early Grades Achievement', href: '/what-we-fund/early-grades-achievement/' },
    { label: 'Educators & Leaders', href: '/what-we-fund/educators-leaders/' },
    { label: 'Our Grantees', href: '/what-we-fund/our-grantees/' },
  ] },
  { label: 'Become Our Partner', href: '/become-our-partner/', key: 'partner', children: [
    { label: 'Grant Application Process', href: '/become-our-partner/grant-application-process/' },
    { label: 'FAQs', href: '/become-our-partner/faqs/' },
  ] },
  { label: 'Contact Us', href: '/contact-us/', key: 'contact' },
];

export const footerNav = nav.map(({ label, href }) => ({ label, href }));

export { site, documents, people, grantees, steps, faqs, reports, news };
