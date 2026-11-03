const $ = selector => document.querySelector(selector);
const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const allowedEmail = value => /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(String(value || ''));
const COLORS = {
  teal: { accent: '#267b77', soft: '#e6f3ee', dark: '#163b4c' },
  navy: { accent: '#244b65', soft: '#e9f1f6', dark: '#132d43' },
  bronze: { accent: '#a27a4a', soft: '#f4f0e9', dark: '#373b43' }
};

function safeWebsite(raw) {
  let input = String(raw || '').trim();
  if (!input) return null;
  if (!/^https?:\/\//i.test(input)) input = 'https://' + input;
  try {
    const parsed = new URL(input);
    if (parsed.protocol !== 'https:' || !parsed.hostname.includes('.') || parsed.username || parsed.password || parsed.port || /[\s<>]/.test(parsed.hostname)) return null;
    const hostname = parsed.hostname.toLowerCase();
    if (/^(?:127\.|0\.|10\.|192\.168\.|localhost$)/.test(hostname)) return null;
    return { href: parsed.href, label: hostname.replace(/^www\./, '') };
  } catch { return null; }
}

function makeSignature(style, details) {
  const name = escapeHtml(details.name || 'Your name');
  const title = escapeHtml(details.title || 'Your title');
  const company = escapeHtml(details.company || 'Your company');
  const email = allowedEmail(details.email) ? String(details.email).trim() : 'hello@example.com';
  const phone = String(details.phone || '').replace(/[^+0-9() .-]/g, '').slice(0, 30);
  const tel = phone.replace(/[^+0-9]/g, '');
  const site = safeWebsite(details.website ?? 'example.com');
  const theme = COLORS[details.accent] || COLORS.teal;
  const mediaRoot = 'https://github505050.github.io/web-studio/assets/';
  const linkStyle = `color:${theme.accent};text-decoration:none;`;
  const mainStyle = 'font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.5;color:#384d5b;border-collapse:collapse;';
  const emailLink = `<a href="mailto:${escapeHtml(email)}" style="${linkStyle}">${escapeHtml(email)}</a>`;
  const phoneLink = tel ? `<a href="tel:${escapeHtml(tel)}" style="${linkStyle}">${escapeHtml(phone)}</a>` : '';
  const websiteLink = site ? `<a href="${escapeHtml(site.href)}" style="${linkStyle}">${escapeHtml(site.label)}</a>` : '';
  const contactLine = [emailLink, phoneLink].filter(Boolean).join('<span style="color:#a3b3b6"> &nbsp;·&nbsp; </span>');
  const siteLine = websiteLink ? `<tr><td style="padding-top:7px">${websiteLink}</td></tr>` : '';
  const normalizedStyle = ['minimal','modern','corporate'].includes(style) ? style : 'minimal';

  if (normalizedStyle === 'minimal') {
    return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="${mainStyle}"><tr><td style="font-size:18px;font-weight:bold;letter-spacing:-.02em;color:${theme.dark};padding:0 0 4px">${name}</td></tr><tr><td style="color:#627782;padding:0 0 12px">${title} &nbsp;|&nbsp; ${company}</td></tr><tr><td style="padding:12px 0 2px;border-top:2px solid ${theme.accent}">${contactLine}</td></tr>${siteLine}</table>`;
  }
  if (normalizedStyle === 'modern') {
    return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="${mainStyle}"><tr><td valign="top" style="padding:0 15px 0 0"><img src="${mediaRoot}sample-avatar.png" alt="Fictional sample portrait illustration" width="72" height="72" style="display:block;width:72px;height:72px;border:0;border-radius:11px"></td><td valign="top" style="padding:0 0 0 16px;border-left:3px solid ${theme.accent}"><table role="presentation" cellpadding="0" cellspacing="0" border="0" style="${mainStyle}"><tr><td style="font-weight:bold;color:${theme.dark};font-size:17px;padding:0 0 3px">${name}</td></tr><tr><td style="color:#637780;padding:0 0 8px">${title} · ${company}</td></tr><tr><td>${contactLine}</td></tr>${siteLine}</table></td></tr></table>`;
  }
  return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="${mainStyle}"><tr><td valign="top" style="padding:0 18px 0 0;border-right:1px solid #d5e2df"><img src="${mediaRoot}sample-logo.png" alt="Fictional sample company logo" width="76" height="76" style="display:block;width:76px;height:76px;border:0"></td><td valign="top" style="padding:0 0 0 18px"><table role="presentation" cellpadding="0" cellspacing="0" border="0" style="${mainStyle}"><tr><td style="font-weight:bold;color:${theme.dark};font-size:17px;padding:0 0 3px">${name}</td></tr><tr><td style="padding:0 0 9px;color:#657984">${title} | ${company}</td></tr><tr><td style="padding-bottom:4px">${contactLine}</td></tr>${siteLine}</table></td></tr></table>`;
}

const tool = $('[data-signature-tool]');
if (tool) {
  const form = $('[data-signature-form]');
  const iframe = $('[data-signature-frame]');
  const code = $('[data-signature-code]');
  const alert = $('[data-signature-message]');
  const styleCards = [...document.querySelectorAll('[data-style-option]')];
  const samples = {
    minimal: { name: 'Alex Morgan', title: 'Creative Director', company: 'North Peak Studio' },
    modern: { name: 'Jordan Lee', title: 'Customer Experience Lead', company: 'Morrow Digital' },
    corporate: { name: 'Taylor Brooks', title: 'Operations Manager', company: 'Cedar Group' }
  };
  let markup = '';
  const refresh = () => {
    const data = Object.fromEntries(new FormData(form));
    markup = makeSignature(data.style, data);
    const localPreview = markup.replaceAll('https://github505050.github.io/web-studio/assets/', '/web-studio/assets/');
    iframe.srcdoc = `<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body style="padding:6px;margin:0;background:white">${localPreview}</body></html>`;
    code.textContent = markup;
    styleCards.forEach(card => card.setAttribute('aria-pressed', String(card.dataset.styleOption === data.style)));
    alert.textContent = safeWebsite(data.website) ? 'Live preview updated. Sample data stays in this browser.' : 'Website is invalid or not HTTPS. It will be omitted from the exported HTML.';
  };
  const setStyle = style => {
    form.elements.namedItem('style').value = style;
    const sample = samples[style];
    if (sample) ['name','title','company'].forEach(key => { form.elements.namedItem(key).value = sample[key]; });
    refresh();
  };
  styleCards.forEach(card => card.addEventListener('click', () => setStyle(card.dataset.styleOption)));
  form.elements.namedItem('style').addEventListener('change', event => setStyle(event.target.value));
  form.addEventListener('input', refresh);
  form.addEventListener('change', refresh);

  $('[data-signature-copy]').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(markup);
      alert.textContent = 'HTML copied. Paste it using your email client’s supported signature method.';
    } catch {
      code.hidden = false;
      const toggle = $('[data-signature-toggle]');
      toggle.setAttribute('aria-expanded','true');
      toggle.textContent = 'Hide HTML';
      alert.textContent = 'Clipboard access is unavailable here. Select the visible HTML and copy it manually.';
    }
  });

  $('[data-signature-download]').addEventListener('click', () => {
    const file = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>HTML email signature sample</title></head><body>${markup}</body></html>`;
    const url = URL.createObjectURL(new Blob([file], { type: 'text/html;charset=utf-8' }));
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'sample-email-signature.html';
    anchor.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    alert.textContent = 'HTML file downloaded. Test it in your target email client before use.';
  });

  $('[data-signature-toggle]').addEventListener('click', event => {
    code.hidden = !code.hidden;
    event.currentTarget.setAttribute('aria-expanded', String(!code.hidden));
    event.currentTarget.textContent = code.hidden ? 'View HTML' : 'Hide HTML';
  });
  refresh();
}
export { makeSignature, allowedEmail, safeWebsite };
