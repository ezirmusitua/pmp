% rebase('templates/base', title='Login')
<section class="main-container">
<div class="form-container">
    <form method="POST" class="login-form" name="login">
        <div>
            <label for="username">Username</label>
            <input name="username"/>
        </div>
        <div>
            <label for="password">Password</label>
            <input name="password" type="password"/>
        </div>
        <button type="submit">Login</button>
    </form>
</div>
</section>
