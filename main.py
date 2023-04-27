from manim import *


def create_vector(d, direction):
    squares = [Square().set_opacity(0.3) for _ in range(d)]
    return VGroup(*squares).arrange(direction, buff=0)


def create_vectors(n, d, group_direction=RIGHT, vector_direction=RIGHT):
    vectors = [create_vector(d, vector_direction) for _ in range(n)]
    return VGroup(*vectors).arrange(group_direction, buff=2.0)


class ConvolutionOverWordVectors(Scene):
    def construct(self):
        # inputs
        sentence = "not all heroes wear capes"
        K = 3  # kernel size,  must be an odd number >= 1
        D = 4  # dimensionality of the vectors

        words = sentence.split()
        N = len(words)

        # write words
        text = Tex(*words, arg_separator=" ")
        self.play(Write(text))
        self.wait()

        # create vectors
        vectors = (
            create_vectors(N, D)
            .set_color(GREEN)
            .scale_to_fit_width(config.frame_width * 0.85 * N / (N + K - 1))
        )
        self.play(*[FadeTransform(text[i], vectors[i]) for i in range(N)])
        self.wait()

        # convolve anim
        def convolve(in_vectors, out_color):
            # create output vectors
            out_vectors = in_vectors.copy().move_to(DOWN).set_color(out_color)

            # create kernel rectangle
            kernel = SurroundingRectangle(in_vectors[:K]).move_to(
                in_vectors[0].get_center()
            )
            self.play(Create(kernel))

            for i in range(N):
                self.play(kernel.animate.move_to(in_vectors[i].get_center()))
                self.play(FadeIn(out_vectors[i]))
                self.wait(0.3)

            self.play(FadeOut(kernel), FadeOut(in_vectors))
            self.remove(kernel, out_vectors)

            # place out vectors where input vectors where
            self.play(out_vectors.animate.move_to(in_vectors.get_center()))

            return out_vectors

        self.play(vectors.animate.shift(UP))
        convolve(convolve(vectors, RED), BLUE)
