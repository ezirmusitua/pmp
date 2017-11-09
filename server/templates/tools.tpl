% rebase('templates/base', title='Stats')
<section class="main-container">
    % for tool in tools:
    <article class="tool-container">
        <h3>{{tool.name}}</h3>
        <ul>
            % for key in tool.display:
            <li><p>{{key}}<span>{{tool.display[key]}}</span></p></li>
            % end
        </ul>
    </article>
    % end
    <article class="tool-container">
        <h3>Proxy Anonymity Detector</h3>
        <ul>
            <li><p>REMOTE ADDRESS: <span>127.0.0.1</span></p></li>
            <li><p>HTTP VIA: <span>127.0.0.1</span></p></li>
            <li><p>HTTP X FORWARDED FOR: <span>127.0.0.1</span></p></li>
        </ul>
        <p>Proxy Anonymity: <span>Elite</span></p>
    </article>
</section>
