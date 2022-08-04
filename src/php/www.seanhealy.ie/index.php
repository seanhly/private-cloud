<?php require_once 'header.php'; ?>
<section style=float:right id=blank>
<h2>Contact</h2>
<table id=contact>
<tr>
	<td>a:</td>
	<td>
		<address>
			ADAPT Centre Office (middle row, by the window)<br>
			School of Computing<br>
			DCU Glasnevin Campus
		</address>
	</td>
</tr>
<tr>
	<td>e:</td>
	<td>
		<a href=mailto:sean.healy@adaptcentre.ie id=email style=font-size:1.5em;>sean.healy@adaptcentre.ie</a>
		<details class="minimal">
			<summary>Email encryption</summary>
			<p>
			You can also send me encrypted emails.
			To do this, you'll first need <a
				href="https://keys.openpgp.org/vks/v1/by-fingerprint/327AC489FF2F8FD4A44749200289DB91C89E5A42"
				target=_blank
   			>my public GPG key</a>.

			After encrypting an email using this key, only I will be able to read the
			content and attachments.
			<p>
			You can encrypt emails moderately easily using popular email programs like
			<a href=https://www.thunderbird.net/ target=_blank>Thunderbird</a>.  There
			are plenty of guides on how to get set up using encrypted email.  E.g.
			<ol>
			<li>
				<a
					href="https://support.mozilla.org/en-US/kb/introduction-to-e2e-encryption"
					target=_blank
				>Introduction to End-to-end encryption in Thunderbird</a>
			<li>
				<a
					href="https://support.mozilla.org/en-US/kb/openpgp-thunderbird-howto-and-faq"
					target=_blank
				>OpenPGP in Thunderbird - HOWTO and FAQ</a>
			<li>
				<a
					href=https://en.wikipedia.org/wiki/End-to-end_encryption
					target=_blank
				>End-to-end encryption on Wikipedia</a>
			</ol>
		</details>
	</td>
</tr>
<tr>
	<td>p:</td>
	<td>
		+353 89 ___ ____<br>
		(<a href="mailto:sean.healy@adaptcentre.ie?subject=Phone Number Request&body=Hi Seán, I'd like to know your phone number.  Could you please send it to me?">request my full number via email</a>)
	</td>
</tr>
<tr>
	<td></td>
	<td>
		<h4>More Contact Info</h4>
		<ul>
			<li> I work at my office address between 8am and 4pm, Monday to Friday.
			<li> My pronouns are he/him.
			<li> My preferred forms of communication:
				<ol>
					<li> Face-to-face (for anything that requires quick back-and-forth).
					<li> Email (for status updates, specs, inter-department collaboration).
					<li> Phone (when <em>face-to-face</em> is not an option).
				</ol>
			<li> Regarding phone, I'd recommend contacting me through
			 	 <a target=_blank href="https://signal.org/download/"
			 	 >Signal</a>, since it's usually cheaper than SMS and regular phone calls.
		</ul>
	</td>
</tr>
</table>
<style>
<?php require_once 'style.css'; ?>
</style>
<h2>Experience</h2>
<h3>Oct 2021&#x2013;Present</h3>
<details>
	<summary>
		<b>PhD Candidate, <a href="https://www.adaptcentre.ie/" target=_blank>ADAPT Centre</a></b>
	</summary>
	<p>
	My research focuses on problems of intersectionality in fair personalised
	information retrieval (IR) systems.  Current fair solutions in machine
	learning and IR are often ill-suited to address more nuanced forms of
	bias, such as discrimination against subsections of larger protected
	groups.  In my research, I develop and study novel algorithms and
	systems with a focus on protecting intersectional groups from biased
	treatment.
</details>
<p>
<h3>Nov 2020&#x2013;Oct 2021</h3>
<details>
	<summary>
		<b>Software developer, <a href="https://www.edgetier.com/" target=_blank>EdgeTier</a></b>
	</summary>
	<ol>
    <li>At EdgeTier I primary worked on fulltext search and indexing.  In
    the process, I gained a deep understanding of PostgreSQL, along with
    Python search and ORM libraries.
    <li>I also contributed heavily towards the abstraction of EdgeTier's
    backend system in order to support a multi-tenanted architecture.
    This is a direction any <em>SaaS</em> company must take in order to
    speed up the onboarding of new clients.
	</ol>
</details>
<p>
<h3>Apr 2019&#x2013;Nov 2020</h3>
<details>
	<summary>
	<b>Full-stack software engineer, <a href="https://vsware.ie/" target=_blank>VSware</a> (acquired by <a href="https://www.visma.com/" target=_blank>Visma</a>)</b>
	</summary>
	<ol>
	<li>I improved several data-intensive endpoints,
	including InSchool&rsquo;s roll call and absence registration
	pages.  These pages are used by teachers across the Norwegian public
	secondary school system (taking roll call with a tablet
	or computer).  My enhancements, taking load times
	from multiple seconds to milliseconds in many cases, has at this
	stage saved Norwegian teachers days of <i>buffering time</i> at the
	beginning of class.</li>
	<li>I was the <code>bash</code> and <code>regex</code> <i>guy</i> in the office,
	often tasked with writing scripts to modify huge portions of code, automate
	tedious tasks, or enforce a coding standard rule across different
	languages.  I led the charge in transitioning date and time standards used
	within Visma&rsquo;s InSchool project to ISO-8601.  This involved huge
	collaboration across teams.</li>
	</ol>
</details>
<p>
<h3>Nov 2018&#x2013;Apr 2019</h3>
<details>
	<summary>
	<b>Software engineer, <a href="https://www.datalex.com/" target=_blank>Datalex</a></b>
	</summary>
	<ol>
	<li>I worked on the airline pricing team, and wrote a web crawler to download,
	index, and cluster pricing rule documentation (tens of thousands of pages
	of legalese text).  This aided other software engineers in retrieving
	important information, and recognising related yet vague terms such as
	&rsquo;Category 4 fare&rsquo; and &rsquo;Record 3&rsquo;.</li>
	<li>I pointed out issues with a deletion procedure on the Linux servers used by
	the pricing team.  The Linux kernel keeps an unlisted copy of a deleted
	file until every program reading that file has closed it.  For
	months, Datalex&rsquo;s QA servers kept running out of disk space, despite deletion
	procedures in place to remove old files.  My Linux knowledge got to the
	bottom of this <i>unexplainable</i> bug.</li>
	</ol>
</details>
<h3>Oct 2017&#x2013;Oct 2018</h3>
<details>
	<summary>
	<b>Full-stack software developer, <a href="https://www.webio.com/" target=_blank>Webio</a></b>
	</summary>
	<ol>
	<li>I improved Webio&rsquo;s underlying REST API&rsquo;s readability and
	maintainability, measured by a 40% reduction in lines of code, by
	introducing object orientation and static utility functions in
	areas with code repetition.</li>
	<li>I increased sales to new clients by rapidly creating high-demand
	features. I successfully oversaw the creation, for example, of a smart
	reply feature, a versioning system for Webio&rsquo;s core functionality (the
	bots creation page), and more mission critical features like the
	ability for human agents to easily intervene in a conversation handled
	by a poorly performing bot.</li>
	</ol>
</details>
<h2>Education</h2>
<h3><a href="http://www.adaptcentre.ie" target=_blank>ADAPT Centre</a> @ <a href="http://www.dcu.ie" target=_blank>Dublin City University</a></h3>
PhD (ongoing)

<a href="http://www.tcd.ie" target=_blank><h3>Trinity College Dublin</h3></a>
<a href="https://www.tcd.ie/slscs/postgraduate/taught-courses/speech-language-processing/" target=_blank><h4>MPhil in Speech and Language Processing</h4></a>

<p>
My dissertation covered privacy-oriented news aggregation.

<a href="https://www.scss.tcd.ie/undergraduate/computer-science-language/" target=_blank><h4>BA in Computer Science, Linguistics and French</h4></a>
<p>
<em>Clubs and societies</em>: Rowing (DUBC), internet society (netsoc), student journalism
<a href="http://u-paris.fr" target=_blank><h3>Université Paris Diderot (now Université de Paris)</h3></a>
<p>
Erasmus student in <i>informatique linguistique</i> (computational
linguistics).  Classes and assignments were through French.  This placement was over
the course of one academic year, as part of my undergraduate degree.

<h2>Languages</h2>
<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">
<colgroup>
<col/>
<col/>
</colgroup>
<tbody>
<tr>
<td>English</td>
<td>First language</td>
</tr>
<tr>
<td>French</td>
<td>Professional working proficiency</td>
</tr>
<tr>
<td>Irish</td>
<td>Good reading and listening.</td>
</tr>
</tbody>
</table>
<h2>References</h2>
<blockquote>
&ldquo;Seán is a self directed learner who sets the highest standards for
himself and others.  Very focused, very motivated, and an excellent
developer.  He makes the difference because he goes the distance.  There is
no mountain he will not climb.  We had a lot of mountains.&rdquo;
</blockquote>
<ol>
<li>Quote by Paul Sweeney<br/>
EVP of Product at Webio, Co-founder of ConverCon</li>
<li>David Power<br/>
Technical Team Lead at Webio</li>
<li>Dr. Tim Fernando<br/>
Lecturer and undergraduate dissertation supervisor</li>
</ol>
<!--a href=https://projecteuler.net/profile/seanhly.png target=_blank><img src=/thumbnails/763946457.png></a-->
</section>
