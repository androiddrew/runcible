<template>
  <div id="app">
    <header>
      <div class="avatar">
        <img
          src="https://www.gravatar.com/avatar/b752c5a6a6e9a34d5bd0a065704d5a40?s=100&d=mm"
          alt
        />
      </div>
    </header>
    <nav>
      <router-link to="/">
        <unicon height="0.9em" name="home" fill="#fff" />Home
      </router-link>
      <router-link to="/ping">
        <unicon height="0.9em" name="cloud-wifi" fill="#fff" />Ping
      </router-link>
      <router-link to="/about">
        <unicon height="0.9em" name="question-circle" fill="#fff" />About
      </router-link>
    </nav>
    <section>
      <transition name="fade">
        <router-view />
      </transition>
    </section>
    <!--<footer>Footer</footer>-->
  </div>
</template>

<style lang="scss">
$nav-bg-color: #333;
$header-bg-color: #5c666f;

html {
  box-sizing: border-box;
  height: 100%;
}
body {
  height: 100%;
  margin: 0;
}
#app {
  height: 100%;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: 70px auto;
}

header {
  z-index: 10;
  text-align: right;
  justify-content: right;
  box-shadow: 0 3px 2px 0 rgba(50, 50, 50, 0.15);
  height: 70px;
  background-color: #5c666f;
  grid-column: 1 / -1;
  img {
    border-radius: 100%;
    margin-top: 10px;
    margin-right: 10px;
    box-shadow: 0 5px 10px 0 rgba(50, 50, 50, 0.5);
    height: 50px;
    width: 50px;
    border-left: 1px solid #fff;
  }
  div {
    display: inline-block;
  }
}

footer {
  z-index: -1;
  height: 60px;
  background-color: grey;
  grid-column: 1 / -1;
}

section {
  padding: 1em 2em;
  grid-column: 3 / -1;
  justify-content: center;
  align-items: center;
}

nav {
  overflow: auto;
  background-color: $nav-bg-color;
  grid-column: 1 / 3;
  box-shadow: 1px 0 2px 0 rgba(50, 50, 50, 0.5);
  a {
    display: block;
    padding-top: 0.5em;
    padding-left: 1.8em;
    text-align: left;
    padding-bottom: 0.5em;
    border-bottom: 1px solid #5c666f;
    /*padding: 20px auto 0 auto;*/
    font-size: 1.2em;
    font-weight: bold;
    color: #fff;
    text-decoration: none;
    &.router-link-exact-active {
      border-left: 0.2em solid darkorange;
      padding-left: 1.6em;
      /*color: darkorange;*/
      /*text-decoration: underline;*/
    }
  }
  a:hover {
    background-color: lighten($nav-bg-color, 5%);
  }
}
.avatar {
  height: 70px;
  width: 70px;
  border-left: 1px solid lighten($header-bg-color, 10%);
}
</style>
