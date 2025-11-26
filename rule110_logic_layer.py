from manim import *
import numpy as np

# ---- Rule 110 update rule (for completeness, though we only use one row here) ----
RULE_110 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}


def step_rule110(row: np.ndarray) -> np.ndarray:
    new = np.zeros_like(row)
    N = len(row)
    for i in range(N):
        left = row[(i - 1) % N]
        center = row[i]
        right = row[(i + 1) % N]
        new[i] = RULE_110[(left, center, right)]
    return new


class Rule110LogicLayer(Scene):
    def construct(self):
        width = 18
        group_size = 3
        cell_size = 0.35

        # ---- precompute some Rule 110 rows ----
        row0 = np.zeros(width, dtype=int)
        row0[width // 2] = 1
        steps = 6
        rows = [row0]
        for _ in range(steps - 1):
            rows.append(step_rule110(rows[-1]))

        # ---- draw Rule 110 rows (bottom = earliest, top = latest) ----
        rule110_group = VGroup()
        for r_index, row in enumerate(rows):
            row_group = VGroup()
            for i, bit in enumerate(row):
                sq = Square(side_length=cell_size)
                sq.set_stroke(GREY_D, width=0.75)
                sq.set_fill(WHITE if bit == 1 else BLACK, opacity=1.0)
                sq.move_to(
                    np.array([
                        (i - width / 2) * cell_size * 1.05,
                        (r_index - (steps - 1) / 2) * cell_size * 1.05 - 2.0,
                        0,
                    ])
                )
                row_group.add(sq)

            # store bits for this row
            setattr(row_group, "bits", np.array(row, dtype=int))
            rule110_group.add(row_group)

        self.play(FadeIn(rule110_group), run_time=1)

        # ---- label under the grid ----
        rule_label = Text(
            "Rule 110 rows (updating in place each frame)",
            font_size=26
        )
        rule_label.next_to(rule110_group, DOWN, buff=0.4)
        self.play(Write(rule_label), run_time=0.7)

        # ---- arrow + text for CURRENT row (visually tracked on TOP row) ----
        current_row_arrow = Arrow(
            start=rule110_group[-1].get_right() + RIGHT * 0.2 + DOWN * 0.2,
            end=rule110_group[-1].get_right() + RIGHT * 0.2 + UP * 0.3,
            buff=0.05,
            stroke_width=2,
        )
        current_row_text = Text("current  row", font_size=22)
        current_row_text.next_to(current_row_arrow, RIGHT, buff=0.1)
        self.play(Create(current_row_arrow), Write(current_row_text), run_time=0.7)

        # ---- static interface line above the grid ----
        interface_y = rule110_group[-1].get_top()[1] + 0.8
        interface_line = Line(
            start=np.array([rule110_group.get_left()[0] - 0.3, interface_y, 0]),
            end=np.array([rule110_group.get_right()[0] + 0.3, interface_y, 0]),
            stroke_width=2,
            color=WHITE,
        )
        self.play(Create(interface_line), run_time=0.7)

        # ---- current logic outputs (dots over TOP row, one per cell) ----
        outputs = []
        outputs_y = interface_y + 1.25
        # treat TOP row as the row whose neighborhoods we visualize
        current_bits = rule110_group[-1].bits

        # For scientific accuracy: use the true Rule 110 neighborhood
        # (b_{j-1}, b_j, b_{j+1}) for every cell j.
        for j in range(width):
            left = current_bits[(j - 1) % width]
            center = current_bits[j]
            right = current_bits[(j + 1) % width]
            val = RULE_110[(left, center, right)]

            cell = rule110_group[-1][j]
            x_pos = cell.get_center()[0]

            dot = Dot(
                point=np.array([x_pos, outputs_y, 0]),
                radius=0.06,
                color=WHITE if val == 1 else GREY_D,
            )
            outputs.append(dot)

        outputs_group = VGroup(*outputs)
        self.play(FadeIn(outputs_group), run_time=1.0)

        outputs_label = Text(
            "Local update rule (evaluated across the row):",
            font_size=26
        )
        outputs_label.next_to(outputs_group, UP, buff=0.5)
        self.play(Write(outputs_label), run_time=0.7)

        # vertical layout factors
        vert_span = outputs_y - interface_y
        arrow_start_factor = 0.10
        arrow_end_factor = 0.45
        label_factor = 0.72

        # ---- brace + arrow on TOP row (for highlighting) ----
        # Use a center index so the brace highlights (b_{i-1}, b_i, b_{i+1})
        example_center_index = width // 2
        example_indices = [
            (example_center_index - 1) % width,
            example_center_index,
            (example_center_index + 1) % width,
        ]
        # Highlight these three cells on the TOP row (about to disappear)
        example_cells = VGroup(*[rule110_group[-1][k] for k in example_indices])
        example_output = outputs[example_center_index]

        brace_cells = Brace(example_cells, direction=UP, buff=0.05)
        brace_text = MathTex(r"(b_{i-1}, b_i, b_{i+1})", font_size=22)
        brace_text.next_to(brace_cells, UP, buff=0.15)

        arrow_x = example_cells.get_center()[0]
        arrow_start_y = interface_y + arrow_start_factor * vert_span
        arrow_end_y = interface_y + arrow_end_factor * vert_span
        arrow_to_output = Arrow(
            start=np.array([arrow_x, arrow_start_y, 0]),
            end=np.array([arrow_x, arrow_end_y, 0]),
            buff=0.05,
            stroke_width=2,
        )

        self.play(Create(brace_cells), Write(brace_text), run_time=0.8)
        self.play(Create(arrow_to_output), run_time=0.6)

        # ---- "output = f(...)" BETWEEN arrow and dots ----
        output_func_under_dot = MathTex(
            r"\text{output} = f(b_{i-1}, b_i, b_{i+1})",
            font_size=20,
            color=GREY_C
        )
        label_y = interface_y + label_factor * vert_span
        output_func_under_dot.move_to(np.array([arrow_x, label_y, 0]))
        output_func_under_dot.set_z_index(10)
        self.play(FadeIn(output_func_under_dot), run_time=0.4)

        self.play(
            example_cells.animate.set_fill(YELLOW, opacity=0.8),
            example_output.animate.set_color(YELLOW),
            run_time=0.7
        )

        self.wait(0.5)

        # ---- Title (centered at top) + subtle X handle underneath ----
        title = Text("Rule 110 — How a Simple Pattern Computes", font_size=38)
        title.to_edge(UP, buff=0.7)

        # Almost-transparent X handle, tucked under the word "Computes"
        x_handle = Text("@wiktoriapawlak_", font_size=20, color=GREY_E)
        # Slightly more visible tag
        x_handle.set_opacity(0.75)
        x_handle.next_to(title, DOWN, buff=0.15).align_to(title, RIGHT)

        self.play(FadeIn(title), FadeIn(x_handle), run_time=0.6)

        # ---- animation of Rule 110 rows (BOTTOM row = current) ----
        def compute_outputs_from_bits(bits):
            """Apply the true Rule 110 neighborhood to every cell in the row."""
            vals = []
            for j in range(width):
                left = bits[(j - 1) % width]
                center = bits[j]
                right = bits[(j + 1) % width]
                vals.append(RULE_110[(left, center, right)])
            return vals

        num_demo_steps = 40
        groups_total = width
        arrow_shown = True
        for step_idx in range(num_demo_steps):
            # next state from BOTTOM row
            next_bits_bottom = step_rule110(rule110_group[0].bits.copy())

            # shift history UP: each row takes bits from the row BELOW it
            for gi in range(len(rule110_group) - 1, 0, -1):
                rule110_group[gi].bits = rule110_group[gi - 1].bits.copy()
            # new state goes to the BOTTOM row
            rule110_group[0].bits = next_bits_bottom.copy()

            # update cell colors
            cell_anims = []
            for gi, rg in enumerate(rule110_group):
                bits = rg.bits
                for i, sq in enumerate(rg):
                    target_color = WHITE if bits[i] == 1 else BLACK
                    cell_anims.append(sq.animate.set_fill(target_color, opacity=1.0))

            # update output dots from TOP row (to match the yellow window)
            new_vals = compute_outputs_from_bits(rule110_group[-1].bits)
            dot_anims = []
            for j, dot in enumerate(outputs):
                new_color = WHITE if new_vals[j] == 1 else GREY_D
                dot_anims.append(dot.animate.set_color(new_color))

            if arrow_shown:
                if step_idx < groups_total:
                    new_group_index = step_idx  # center index i
                    # Three cells: (i-1, i, i+1) on the TOP row (about to disappear)
                    new_indices = [
                        (new_group_index - 1) % width,
                        new_group_index,
                        (new_group_index + 1) % width,
                    ]
                    new_cells = VGroup(*[rule110_group[-1][k] for k in new_indices])
                    new_output = outputs[new_group_index]

                    new_brace = Brace(new_cells, direction=UP, buff=0.05)
                    # Keep the moving brace label consistent with the static one:
                    # neighborhoods are (b_{i-1}, b_i, b_{i+1})
                    new_brace_text = MathTex(
                        r"(b_{i-1}, b_i, b_{i+1})", font_size=22
                    ).next_to(new_brace, UP, buff=0.15)

                    arrow_x = new_cells.get_center()[0]
                    new_start = np.array([
                        arrow_x,
                        interface_y + arrow_start_factor * vert_span,
                        0,
                    ])
                    new_end = np.array([
                        arrow_x,
                        interface_y + arrow_end_factor * vert_span,
                        0,
                    ])

                    # reset previous highlight on TOP row
                    reset_anims = []
                    for sq in example_cells:
                        idx_in_row = list(rule110_group[-1]).index(sq)
                        bit_val = rule110_group[-1].bits[idx_in_row]
                        reset_anims.append(
                            sq.animate.set_fill(WHITE if bit_val == 1 else BLACK, opacity=1.0)
                        )

                    highlight_anims = [c.animate.set_fill(YELLOW, opacity=0.8) for c in new_cells]
                    dot_highlight = [new_output.animate.set_color(YELLOW)]

                    self.play(
                        *(
                            cell_anims
                            + dot_anims
                            + reset_anims
                            + highlight_anims
                            + dot_highlight
                            + [
                                brace_cells.animate.become(new_brace),
                                brace_text.animate.become(new_brace_text),
                                arrow_to_output.animate.put_start_and_end_on(new_start, new_end),
                                output_func_under_dot.animate.move_to(
                                    np.array([
                                        arrow_x,
                                        interface_y + label_factor * vert_span,
                                        0,
                                    ])
                                ),
                            ]
                        ),
                        run_time=0.55,
                    )

                    example_cells = new_cells
                    example_output = new_output

                    if new_group_index == groups_total - 1:
                        clear_highlight = []
                        for sq in example_cells:
                            idx_in_row = list(rule110_group[-1]).index(sq)
                            bit_val = rule110_group[-1].bits[idx_in_row]
                            clear_highlight.append(
                                sq.animate.set_fill(WHITE if bit_val == 1 else BLACK, opacity=1.0)
                            )
                        self.play(
                            *clear_highlight,
                            FadeOut(brace_cells),
                            FadeOut(brace_text),
                            FadeOut(arrow_to_output),
                            FadeOut(output_func_under_dot),
                            run_time=0.35,
                        )
                        arrow_shown = False
                else:
                    self.play(*(cell_anims + dot_anims), run_time=0.45)
            else:
                self.play(*(cell_anims + dot_anims), run_time=0.45)

        self.wait(0.5)

