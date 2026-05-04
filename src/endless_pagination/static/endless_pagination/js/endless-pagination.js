'use strict';

(function (global) {
    const DEFAULTS = {
        containerSelector: '.endless_container',
        loadingSelector: '.endless_loading',
        moreSelector: 'a.endless_more',
        pageSelector: '.endless_page_template',
        pagesSelector: 'a.endless_page_link',
        onClick() {},
        onCompleted() {},
        paginateOnScroll: false,
        paginateOnScrollMargin: 1,
        paginateOnScrollChunkSize: 0,
    };

    const contextOf = (link) => ({
        key: link.getAttribute('rel').split(' ')[0],
        url: link.getAttribute('href'),
    });

    const buildUrl = (url, key) => {
        const separator = url.includes('?') ? '&' : '?';
        return `${url}${separator}querystring_key=${encodeURIComponent(key)}`;
    };

    const fetchFragment = async (url, key) => {
        const response = await fetch(buildUrl(url, key), {
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin',
        });
        if (!response.ok) {
            throw new Error(`endless-pagination: HTTP ${response.status}`);
        }
        return await response.text();
    };

    const parseFragment = (html) => {
        const template = document.createElement('template');
        template.innerHTML = html;
        return template.content;
    };

    class EndlessPagination {
        constructor(element, options) {
            this.element = element;
            this.settings = { ...DEFAULTS, ...(options || {}) };
            this.loadedPages = 1;
            this._busy = new WeakSet();

            this._onClick = this._onClick.bind(this);
            this._onScroll = this._onScroll.bind(this);

            this.element.addEventListener('click', this._onClick);
            if (this.settings.paginateOnScroll) {
                window.addEventListener('scroll', this._onScroll, { passive: true });
            }
        }

        destroy() {
            this.element.removeEventListener('click', this._onClick);
            window.removeEventListener('scroll', this._onScroll);
        }

        _onClick(event) {
            const target = event.target;
            if (!(target instanceof Element)) return;

            const more = target.closest(this.settings.moreSelector);
            if (more && this.element.contains(more)) {
                event.preventDefault();
                this._loadMore(more);
                return;
            }
            const page = target.closest(this.settings.pagesSelector);
            if (page && this.element.contains(page)) {
                event.preventDefault();
                this._loadPage(page);
            }
        }

        async _loadMore(link) {
            const container = link.closest(this.settings.containerSelector);
            if (!container || this._busy.has(container)) return;

            const loading = container.querySelector(this.settings.loadingSelector);
            this._busy.add(container);
            link.style.display = 'none';
            if (loading) loading.style.display = '';

            const context = contextOf(link);
            if (this.settings.onClick.call(link, context) === false) {
                this._busy.delete(container);
                return;
            }

            try {
                const fragment = await fetchFragment(context.url, context.key);
                container.parentNode.insertBefore(parseFragment(fragment), container);
                container.remove();
                this.loadedPages += 1;
                this.settings.onCompleted.call(link, context, fragment.trim());
            } catch (error) {
                this._busy.delete(container);
                if (loading) loading.style.display = 'none';
                link.style.display = '';
                throw error;
            }
        }

        async _loadPage(link) {
            const pageTemplate = link.closest(this.settings.pageSelector);
            if (!pageTemplate) return;

            const context = contextOf(link);
            if (this.settings.onClick.call(link, context) === false) return;

            const fragment = await fetchFragment(context.url, context.key);
            pageTemplate.innerHTML = fragment;
            this.settings.onCompleted.call(link, context, fragment.trim());
        }

        _onScroll() {
            const remaining =
                document.documentElement.scrollHeight -
                window.innerHeight -
                window.scrollY;
            if (remaining > this.settings.paginateOnScrollMargin) return;

            const chunkSize = this.settings.paginateOnScrollChunkSize;
            if (chunkSize && this.loadedPages % chunkSize === 0) return;

            const more = this.element.querySelector(this.settings.moreSelector);
            if (more) more.click();
        }
    }

    const isPlainOptions = (value) =>
        value !== null &&
        typeof value === 'object' &&
        !value.nodeType &&
        typeof value.length !== 'number';

    const resolveTargets = (target) => {
        if (target == null) return [document.body];
        if (typeof target === 'string') {
            return Array.from(document.querySelectorAll(target));
        }
        if (target.nodeType === 1) return [target];
        if (typeof target.length === 'number') return Array.from(target);
        return [];
    };

    function endlessPaginate(target, options) {
        if (isPlainOptions(target)) {
            options = target;
            target = null;
        }
        const instances = resolveTargets(target).map(
            (element) => new EndlessPagination(element, options)
        );
        return instances.length === 1 ? instances[0] : instances;
    }

    global.EndlessPagination = EndlessPagination;
    global.endlessPaginate = endlessPaginate;
})(typeof window !== 'undefined' ? window : this);
