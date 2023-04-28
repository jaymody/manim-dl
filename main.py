from manim import *


def create_vector(d, direction):
    squares = [Square().set_opacity(0.3) for _ in range(d)]
    return VGroup(*squares).arrange(direction, buff=0)


def create_vectors(n, d, group_direction=RIGHT, vector_direction=RIGHT, buff=2.0):
    vectors = [create_vector(d, vector_direction) for _ in range(n)]
    return VGroup(*vectors).arrange(group_direction, buff=buff)


def create_function_circle():
    circle = Circle(
        color=WHITE, stroke_width=DEFAULT_STROKE_WIDTH * 0.5, fill_opacity=0.1
    )
    circle.add(MathTex("f").scale(2.5))
    return circle


class RecurrenceOverWordVectors(Scene):
    def construct(self):
        # inputs
        sentence = "not all heroes wear capes"
        D = 4  # dimensionality of vectors

        words = sentence.split()
        N = len(words)

        # write words
        text = Tex(*words, arg_separator=" ")
        self.play(Write(text))
        self.wait()

        # create vectors
        vectors = (
            create_vectors(N, D, buff=8.0)
            .set_color(GREEN)
            .scale_to_fit_width(config.frame_width * 0.9 * N / (N + 2))
        )
        self.play(*[FadeTransform(text[i], vectors[i]) for i in range(N)])
        self.wait()

        # compute gap distance
        gap_vec = vectors[1].get_center() - vectors[0].get_center()

        # recurrence anim
        def recurrence(in_vectors, out_color, hidden_color, init_hidden_vector=None):
            arrows = VGroup()

            def anim_cell(inp, out, h_in, h_out, cell):
                i_to_f = Arrow(inp.get_top(), cell.get_bottom(), buff=0.1)
                h_to_f = Arrow(h_in.get_right(), cell.get_left(), buff=0.1)

                f_to_o = Arrow(cell.get_top(), out.get_bottom(), buff=0.1)
                f_to_h = Arrow(cell.get_right(), h_out.get_left(), buff=0.1)

                arrows.add(i_to_f, h_to_f, f_to_o, f_to_h)

                self.play(FadeIn(cell), FadeIn(i_to_f), FadeIn(h_to_f))
                self.play(FadeIn(out), FadeIn(h_out), FadeIn(f_to_o), FadeIn(f_to_h))

            out_vectors = in_vectors.copy().shift(2 * UP).set_color(out_color)

            if init_hidden_vector is None:
                init_hidden_vector = (
                    in_vectors[0]
                    .copy()
                    .set_color(hidden_color)
                    .arrange(DOWN, buff=0)
                    .move_to(in_vectors[0].get_center() - 0.5 * gap_vec + UP * 1)
                )
            hidden_vectors = VGroup(
                *[init_hidden_vector.copy().shift(i * gap_vec) for i in range(N + 1)]
            )

            cells = VGroup(
                *[
                    create_function_circle()
                    .move_to(v.get_center() + 0.5 * gap_vec)
                    .set_color(WHITE)
                    .scale_to_fit_width(v.get_height() * 0.5)
                    for v in hidden_vectors[:-1]
                ]
            )

            self.play(FadeIn(hidden_vectors[0]))
            for i in range(N):
                anim_cell(
                    in_vectors[i],
                    out_vectors[i],
                    hidden_vectors[i],
                    hidden_vectors[i + 1],
                    cells[i],
                )

            final_hidden_vector = hidden_vectors[-1]
            self.play(
                FadeOut(cells),
                FadeOut(hidden_vectors[:-1]),
                FadeOut(in_vectors),
                FadeOut(arrows),
            )
            self.play(
                final_hidden_vector.animate.move_to(hidden_vectors[0].get_center())
            )
            self.play(out_vectors.animate.move_to(in_vectors.get_center()))

            self.remove(cells, hidden_vectors[:-1], in_vectors, arrows)
            return out_vectors, final_hidden_vector

        self.play(vectors.animate.shift(DOWN))
        vectors, init_hidden_vector = recurrence(vectors, RED, ORANGE, None)
        vectors, _ = recurrence(vectors, BLUE, ORANGE, init_hidden_vector)


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
