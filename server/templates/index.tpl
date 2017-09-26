% rebase('templates/base', title='Proxy List')
<section>
    <article>
        <table>
            <caption>Proxy List / 1</caption>
            <tr>
                <th>ip address</th>
                <th>port</th>
                <th>anonymity</th>
                <th>location</th>
                <th>last check</th>
                <th>available sites</th>
            </tr>
            % for i in range(0, 10):
            <tr>
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
    <article>
        <p>Total Page: 999</p>
        <nav>
            <form>
                <fieldset>
                    <a href="2">Next Page</a>
                </fieldset>
                <fieldset>
                    <a href="1">Previous Page</a>
                </fieldset>
                <fieldset>
                    <input title="Jump To Page" type="number">
                    <button>Go</button>
                </fieldset>
            </form>
        </nav>
    </article>
</section>