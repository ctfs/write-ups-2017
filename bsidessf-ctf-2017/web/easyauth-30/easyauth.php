<?php
  require_once('./auth.php');

  if(isset($_GET['action']) && $_GET['action'] === 'logout') {
    setcookie('auth', '');
    header('Location: index.php');
    exit(0);
  }

  if(isset($_POST['username'])) {
    # Do pagey stuff
    if(is_valid($_POST['username'], $_POST['password'])) {
      # Create the cookie
      $cookie = 'username=' . $_POST['username'] . '&';
      $cookie .= 'date=' . date(DATE_ISO8601) . '&';

      setcookie('auth', $cookie);
      print "<h1>Login successful!</h1>\n";
      print "<p>Setting cookie: <tt>auth=$cookie</tt></p>\n";
    } else {
      print "<h1>Username or password was incorrect!</h1>\n";
    }
    print "<p>Click <a href='index.php'>here</a> to continue!</p>\n";
    exit(0);
  }

  if(!isset($_COOKIE['auth'])) {
    require_once('./login_form.php');
    exit(0);
  }
  $cookie = $_COOKIE['auth'];

  $pairs = explode('&', $cookie);
  $args = array();
  foreach($pairs as $pair) {
    if(!strpos($pair, '='))
      continue;

    list($name, $value) = explode('=', $pair, 2);
    $args[$name] = $value;
  }
  $username = $args['username'];

  print "<h1>Welcome back, $username!</h1>\n";
  if($username == 'administrator') {
    print "<p>Congratulations, you're the administrator! Here's your reward:</p>\n";
    print "<p>" . FLAG . "</p>\n";
  } else {
    print "<p>It's cool that you logged in, but unfortunately we can only give the flag to 'administrator'. :(</p>\n";
  }
  print "<p><a href='/index.php?action=logout'>Log out</a></p>\n";
?>
