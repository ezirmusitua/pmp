% rebase('templates/base', title='Proxy List')
<section class="main-container">
    <article>
        <table class="proxy-list__table">
            <caption>Proxy List / 1</caption>
            <tr class="proxy-list__table-header">
                <th>ip address</th>
                <th>port</th>
                <th>anonymity</th>
                <th>location</th>
                <th>last check</th>
                <th>available sites</th>
            </tr>
            % for i in range(0, 10):
            <tr class="proxy-list__table-item">
                <td>127.0.0.1</td>
                <td>8080</td>
                <td>elite</td>
                <td>China, Shanghai</td>
                <td>2017-09-26 23:00:00</td>
                <td>Show</td>
            </tr>
            % end
        </table>
    </article>
    <article class="pagination__container">
        <form class="pagination__control-form">
            <button><a href="2">Next Page</a></button>
            <fieldset>
                <input title="Jump To Page" type="number">
                <button>Go</button>
            </fieldset>
            <button><a href="1">Previous Page</a></button>
        </form>
        <p>Total Page: 999</p>
    </article>
</section>