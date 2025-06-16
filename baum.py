from manim import *

def draw_full_tree(scene, root_pos, depth=3):
    vert = 1.5
    horiz1 = 3.0
    horiz2 = 1.2
    dots = []
    labels = []
    level1_labels = []
    edges = []
    triangles = []
    # Draw root
    root = Dot(root_pos)
    label0 = MathTex("R", font_size=48).scale(0.7).next_to(root, LEFT)
    dots.append(root)
    labels.append(label0)
    # Level 1
    level1 = []
    edges1 = []
    for idx, i in enumerate([1, 0, -1]):
        pos = root_pos + DOWN * vert + i * horiz1 * LEFT
        dot = Dot(pos)
        level1.append(dot)
        dots.append(dot)
        label = MathTex(f"v_{idx}", font_size=36).scale(0.7).next_to(dot, LEFT, buff=0.1)
        labels.append(label)
        level1_labels.append(label)
        edge = Line(root_pos, pos)
        edges1.append(edge)
        edges.append(edge)
    # Level 2
    level2 = []
    subtrees = []
    for idx, node in enumerate(level1):
        labels2 = []
        tris2 = []
        children = []
        lines = []
        for jdx, j in enumerate([1, 0, -1]):
            pos = node.get_center() + DOWN * vert + j * horiz2 * LEFT
            child = Dot(pos).scale(0.7)
            children.append(child)
            dots.append(child)
            label = MathTex(f"v_{{{idx}{jdx}}}", font_size=32).next_to(child, LEFT, buff=0.1)
            labels.append(label)
            labels2.append(label)
            edge = Line(node.get_center(), pos)
            lines.append(edge)
            edges.append(edge)
            # Draw triangle at leaf
            gap = 0.2
            v_off = 0.8
            h_off = 0.3
            tri = Polygon(child.get_center() + DOWN * gap,
                          child.get_center() + DOWN * (gap + v_off) + LEFT * h_off,
                          child.get_center() + DOWN * (gap + v_off) + RIGHT * h_off)
            triangles.append(tri)
            tris2.append(tri)
        level2.append(children)
        subtrees.append(VGroup(
            level1[idx], level1_labels[idx],
            *children, *lines, *labels2, *tris2
        ))
    # Add all objects to scene and animate together
    scene.add(*dots, *labels, *edges, *triangles)
    scene.play(
        *[GrowFromCenter(m) for m in dots],
        *[Write(l) for l in labels],
        *[Create(e) for e in edges + triangles],
        run_time=1,
        lag_ratio=0.1
    )
    return level1, level2, subtrees

class BaumSzene(Scene):
    def construct(self):
        # Level 0: Wurzel
        root = Dot(UP * 3)
        label0 = MathTex("R", font_size=48).scale(0.7).next_to(root, LEFT)

        # Level 1: 3 Kinder
        level1 = [
            Dot(UP * 1.5 + i * 3 * LEFT) for i in [1, 0, -1]
        ]
        edges1 = [
            Line(root.get_center(), child.get_center())
            for child in level1
        ]
        labels1 = [
            MathTex(f"v_{i}", font_size=36).next_to(child, LEFT)
            for i, child in enumerate(level1)
        ]

        # Level 2: Je 3 Kinder pro Knoten
        level2 = []
        edges2 = []
        for center in level1:
            children = [
                Dot(center.get_center() + DOWN * 1.5 + i * 1.2 * LEFT)
                for i in [1, 0, -1]
            ]
            level2.append(children)
            edges2 += [
                Line(center.get_center(), child.get_center())
                for child in children
            ]

        # Alles auf die Szene
        self.play(GrowFromCenter(root), Write(label0))
        self.play(*[GrowFromCenter(dot) for dot in level1], *[Write(label) for label in labels1])
        self.play(*[Create(line) for line in edges1])
        for children in level2:
            self.play(*[GrowFromCenter(dot) for dot in children])
        self.play(*[Create(line) for line in edges2])

        for g_idx, children in enumerate(level2):
            for j, node in enumerate(children):
                label = MathTex(f"v_{{{g_idx}{j}}}", font_size=28).next_to(node, LEFT, buff=0.01)
                self.play(Write(label), run_time=0.2)
                # Draw a small isosceles triangle at the leaf
                center = node.get_center()
                gap = 0.2
                v_off = 0.8
                h_off = 0.3
                apex = center + DOWN * gap
                left = center + DOWN * (gap + v_off) + LEFT * h_off
                right = center + DOWN * (gap + v_off) + RIGHT * h_off
                triangle = Polygon(apex, left, right)
                self.play(Create(triangle), run_time=0.2)
        self.wait(1)

class SigmaSzene(Scene):
    def construct(self):
        root_pos = ORIGIN + UP * 3.5
        level1, _, subtrees = draw_full_tree(self, root_pos, depth=3)
        # Positions for permutation
        positions = [node.get_center() for node in level1]
        self.wait(1)
        # Sigma: cyclic shift (1->2->3)
        self.play(*[
            subtrees[i].animate.shift(positions[(i+1) % 3] - level1[i].get_center())
            for i in range(3)
        ], run_time=1)
        self.wait(1)

class SigmaInverseSzene(Scene):
    def construct(self):
        root_pos = ORIGIN + UP * 3.5
        level1, _, subtrees = draw_full_tree(self, root_pos, depth=3)
        positions = [node.get_center() for node in level1]
        self.wait(1)
        # Sigma^{-1}: inverse cyclic shift (1->3->2)
        self.play(*[
            subtrees[i].animate.shift(positions[(i-1) % 3] - level1[i].get_center())
            for i in range(3)
        ], run_time=1)
        self.wait(1)

class OmegaSzene(Scene):
    def construct(self):
        root_pos = ORIGIN + UP * 3.5
        # TODO: implement Omega animation using draw_full_tree
        pass