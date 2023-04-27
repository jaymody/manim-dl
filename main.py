from manim import *


class ConvolutionOverWordVectors(Scene):
    def construct(self):
        def create_vec(color, opacity=None):
            squares = [
                Square(side_length=1, color=color, fill_opacity=0.3).set_opacity(
                    opacity
                )
                for _ in range(4)
            ]
            return Group(*squares).arrange(RIGHT, buff=0)

        def create_vecs(num, w, color):
            left = [create_vec(color, 0.0) for _ in range(w)]
            middle = [create_vec(color) for _ in range(num)]
            right = [create_vec(color, 0.0) for _ in range(w)]
            return Group(*left, *middle, *right).arrange(RIGHT, buff=2.0)

        # inputs
        sentence = "not all heroes wear capes"
        K = 3  # must be an odd number >= 1

        words = sentence.split()
        N = len(words)
        W = (K - 1) // 2

        # write words
        texts = Tex(*words, arg_separator=" ").scale_to_fit_width(width=8).move_to(UP)
        self.play(Write(texts))
        self.wait()

        # create vectors
        vecs = create_vecs(N, W, GREEN).scale_to_fit_width(width=12)
        self.play(*[FadeTransform(texts[i], vecs[i + W]) for i in range(N)])
        self.wait()

        # convolve anim
        def convolve(in_vecs, out_color):
            # move embeddings up
            self.play(in_vecs.animate.shift(UP))
            self.wait()

            # conv
            boxes = []
            for i in range(N):
                rect = SurroundingRectangle(in_vecs[i : i + K])
                boxes.append(rect)

            out_vecs = create_vecs(N, W, out_color).scale_to_fit_width(width=12)

            for i in range(N):
                if i == 0:
                    self.play(Create(boxes[0]))
                else:
                    self.play(ReplacementTransform(boxes[i - 1], boxes[i]))
                self.play(FadeIn(out_vecs[K + i - 2]))
                self.wait(0.5)

            self.play(FadeOut(boxes[-1]), FadeOut(in_vecs))
            self.remove(*boxes, in_vecs)

            return out_vecs

        convolve(convolve(vecs, RED), BLUE)
