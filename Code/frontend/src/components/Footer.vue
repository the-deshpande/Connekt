<script></script>
<template>
	<footer
		class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
		<div class="col-md-4 d-flex align-items-center ps-4">
			<img
				alt="Connekt Logo"
				class="filter-white"
				src="../assets/logo.svg"
				height="24"
				width="24" />
			<span class="mb-3 mb-md-0 text-white px-3">© 2024 Connekt</span>
		</div>

		<ul class="nav col-md-4 justify-content-end list-unstyled d-flex pe-5">
			<li class="ms-3">
				<a
					class="text-muted"
					href="https://www.linkedin.com/in/the-deshpande"
					target="_blank">
					<img
						alt="LinkedIn Logo"
						class="filter-white"
						src="../assets/linkedin-logo.svg" />
				</a>
			</li>
			<li class="ms-3">
				<a
					class="text-muted"
					href="https://www.github.com/the-deshpande"
					target="_blank">
					<img
						alt="Github Logo"
						class="filter-white"
						src="../assets/github-logo.svg" />
				</a>
			</li>
			<li class="ms-3">
				<a
					class="text-muted"
					href="https://www.instagram.com/the_deshpande/"
					target="_blank"></a>
				<img
					alt="Instagram Logo"
					class="filter-white"
					src="../assets/instagram-logo.svg" />
			</li>
		</ul>
	</footer>
</template>

<style lang="scss" scoped>
.filter-white {
	filter: invert(100%) sepia(2%) saturate(1560%) hue-rotate(261deg)
		brightness(115%) contrast(100%);
}
img:hover {
	filter: invert(86%) sepia(21%) saturate(511%) hue-rotate(75deg)
		brightness(93%) contrast(89%);
}
</style>
