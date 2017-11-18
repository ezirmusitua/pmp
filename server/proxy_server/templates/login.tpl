% rebase('templates/base', title='Login')
<section class="main-container">
    <div class="form-container">
        <form method="POST" class="login-form {{'error-box-shadow' if invalid else ''}}" name="login">
            <h4>Login</h4>
            % if invalid:
            <span style="color: red;
            font-size: 12px;
            width: 100%;
            text-align: center;
            margin-top: -16px;
            background-color: rgba(0, 0, 0, 0.04);
            padding: 4px 0;
            border-radius: 4px;">Invalid username or password
            </span>
            % end
            <div class="input-container">
                <label for="username">username</label>
                <input id="username" name="username"/>
            </div>
            <div class="input-container">
                <label for="password">password</label>
                <input id="password" name="password" type="password"/>
            </div>
            <button class="raised-button" type="submit">Login</button>
        </form>
    </div>
</section>
