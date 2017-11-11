% rebase('templates/base', title='Proxy List')
<section class="main-container">
    <article>
        <table class="proxy-list__table">
            <caption>Proxy List / {{pagination['page_index']}}</caption>
            <tr class="proxy-list__table-header">
                <th>ip address</th>
                <th>port</th>
                <th>anonymity</th>
                <th>location</th>
                <th>last check</th>
                <th>available sites</th>
            </tr>
            % for proxy in proxies:
            <tr class="proxy-list__table-item">
                <td>{{proxy.ip_address}}</td>
                <td>{{proxy.port}}</td>
                <td>{{proxy.anonymity}}</td>
                <td>{{proxy.location}}</td>
                <td>{{proxy.last_check_at}}</td>
                <td>{{','.join(proxy.available_sites)}}</td>
            </tr>
            % end
        </table>
    </article>
    <article class="pagination__container">
        <form action="/proxies" class="pagination__control-form">
            <button class="raised-button" style="width: 120px; margin: 4px 8px 4px 0"><a
                    href="/proxies?page-index={{pagination['prev_page']}}">Previous Page</a></button>
            <fieldset>
                <input name="page-index" title="Jump To Page" type="number" value="{{pagination['page_index']}}">
                <button class="raised-button" type="submit">Go</button>
            </fieldset>
            <button class="raised-button" style="width: 120px; margin: 4px 0 4px 8px"><a
                    href="/proxies?page-index={{pagination['next_page']}}">Next Page</a></button>
        </form>
        <p>Total Page: {{pagination['page_count']}}</p>
    </article>
</section>