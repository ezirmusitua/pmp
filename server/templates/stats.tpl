% rebase('templates/base', title='Stats')
<section>
    % for i in range(0, 2):
    <article>
        <h3>Proxy Crawler</h3>
        <div>
            <form>
                <fieldset>
                    <button title="restart crawler">Restart</button>
                </fieldset>
                <fieldset>
                    <button title="stop crawler">Stop</button>
                </fieldset>
            </form>
        </div>
        <div>
            <ul>
                <li>
                    <p>Is Running: <span>Yes</span></p>
                </li>
                <li>
                    <p>Crawled Count: <span>1</span></p>
                </li>
                <li>
                    <p>Dropped Count: <span>1</span></p>
                </li>
            </ul>
        </div>
    </article>
    % end
</section>
