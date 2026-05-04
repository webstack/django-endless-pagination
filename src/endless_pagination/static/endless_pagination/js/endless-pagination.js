'use strict';

(function (global) {
    const DEFAULTS = {
        containerSelector: '.endless_container',
        loadingSelector: '.endless_loading',
        moreSelector: 'a.endless_more',
        paginateOnScroll: false,
        paginateOnScrollMargin: 1,
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
            try {
                const fragment = await fetchFragment(context.url, context.key);
                container.parentNode.insertBefore(parseFragment(fragment), container);
                container.remove();
            } catch (error) {
                this._busy.delete(container);
                if (loading) loading.style.display = 'none';
                link.style.display = '';
                throw error;
            }
        }

        _onScroll() {
            const remaining =
                document.documentElement.scrollHeight -
                window.innerHeight -
                window.scrollY;
            if (remaining > this.settings.paginateOnScrollMargin) return;
            const more = this.element.querySelector(this.settings.moreSelector);
            if (more) more.click();
        }
    }

    function endlessPaginate(options) {
        return new EndlessPagination(document.body, options);
    }

    global.EndlessPagination = EndlessPagination;
    global.endlessPaginate = endlessPaginate;
})(typeof window !== 'undefined' ? window : this);
