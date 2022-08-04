<?php
    $localLinks = [
        #"/contact/" => "Contact",
        #"/cv/" => "Curriculum Vitae",
        #"/fir/" => "FIR Blog",
        "/docmuch/" => "Folksonomy"
    ];
    function hrefIsCurrentPage($href) {
        return "${_SERVER["REQUEST_URI"]}index.php" === $href || $_SERVER["REQUEST_URI"] === $href;
    }
    if (defined('$title')) {
        $title = "Seán Healy - $title";
    } else {
        $title = "Seán Healy's";
        $titleModified = false;
        foreach ($localLinks as $href => $value) {
            if (hrefIsCurrentPage($href)) {
                $title = "$title $value";
                $titleModified = true;
                break;
            }
        }
        if (!$titleModified) {
            foreach ($localLinks as $href => $value) {
                if ($href === substr($_SERVER["REQUEST_URI"], 0, strlen($href))) {
                    $name = preg_replace(
                        "/_/",
                        " ",
                        preg_replace(
                            "/^([0-9]{4})_([0-9]{2})/",
                            "$1-$2",
                            preg_replace(
                                "/^([0-9]{4})_([0-9]{2})_([0-9]{2})/",
                                "$1-$2-$3",
                                preg_split(
                                    "/\//",
                                        $_SERVER["REQUEST_URI"]
                                )[2]
                            )
                        )
                    );
                    $title = "$title's $value / $name";
                    $titleModified = true;
                    break;
                }
            }
            if (!$titleModified) {
                $title = "$title website";
            }
        }
    }
    function nonRedundantLink($href, $value) {
        if (hrefIsCurrentPage($href)) {
            echo "<span id=current>$value</span>";
        } else {
            echo "<a href='$href'>$value</a>";
        }
    }
?>
<!doctype html>
<head>
<link rel="stylesheet" href="/style.css">
<link rel="icon" type="image/png" href="/favicon.png">
<meta charset="utf-8">
<meta name="author" content="Seán Healy">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
 <meta name="keywords" content="personal, webpage, programming, writing, tech, computer, science, linguistics, language, photo, travel">
<title><?php echo $title; ?></title>
<body>
<section>
    <h1 style=margin-bottom:20px><?php nonRedundantLink("/", "Seán Healy"); ?></h1>
    <?php if (hrefIsCurrentPage("/")): ?>
		<img src="/profile.jpg" width=200>
    <?php endif; ?>
	<br>
	<br>
    <!--u style=text-decoration-line:underline;text-decoration-style:double;>A to Z</u-->
    <ul id=sidebar>
        <?php
            foreach ($localLinks as $href => $value) {
                echo "<li>";
                if (substr($href, 0, 1) === "/") {
                    echo "/ ";
                    nonRedundantLink($href, $value);
                } else {
                    echo "<a href='$href' target=_blank>$value</a> &rarr;";
                }
            }
        ?>
    </ul>
</section>
