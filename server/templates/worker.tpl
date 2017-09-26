% rebase('templates/base', title='Stats')
<section class="main-container">
    % for i in range(0, 2):
    <article class="worker-controller__container">
        <h3>Proxy Crawler</h3>
        <div class="worker-controller__actions-bar">
            <p>Actions: </p>
            <form>
                <button title="restart crawler">Restart</button>
                <button title="stop crawler">Stop</button>
            </form>
        </div>
        <div class="worker-controller__stats-bar">
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
