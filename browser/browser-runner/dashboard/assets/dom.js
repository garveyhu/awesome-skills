// dom.js —— DOM 微助手（不引框架，就这几个够用）。

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/** clone 一个 <template> 的首个元素。杜绝字符串拼 HTML。 */
export function tmpl(id) {
  const t = document.getElementById(id);
  if (!t) throw new Error(`缺模板 #${id}`);
  return t.content.firstElementChild.cloneNode(true);
}

/** 建元素：elem('span', 'cls', '文本') → <span class="cls">文本</span>。 */
export function elem(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
}

/** 按 data 槽填文本：fill(root, { title: '...', desc: '...' }) → [data-title]/[data-desc]。 */
export function fill(root, slots) {
  for (const [key, val] of Object.entries(slots)) {
    const node = root.querySelector(`[data-${key}]`);
    if (node) node.textContent = val;
  }
  return root;
}
