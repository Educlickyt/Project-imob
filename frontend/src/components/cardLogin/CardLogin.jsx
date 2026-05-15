import React from 'react'

const CardLogin = () => {
  return (
    <div>
        <form method="post">
            <label htmlFor="login">
                <span>Login:</span>
                <input type="text" name="login" id="login"/>
            </label>
            <label htmlFor="password">
                <span>Senha:</span>
                <input type="password" name="password" id="password"/>
            </label>
        </form>
    </div>
  )
}

export default CardLogin