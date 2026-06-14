# Live Dashboard patch instructions

The `elif page_idx == PAGE_LD:` block at the bottom of `nexus.py` is
incomplete (truncated at the 52-week high lookup).

Replace **everything** from `elif page_idx == PAGE_LD:` to the end of the
file with the two lines below:

```python
elif page_idx == PAGE_LD:
    from live_dashboard_page import render_live_dashboard
    render_live_dashboard(sel_companies)
```

The full implementation lives in `live_dashboard_page.py` (just committed).
