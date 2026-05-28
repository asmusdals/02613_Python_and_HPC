import multiprocessing
import os
import tempfile

import numpy as np


def mandelbrot_escape_time(c):
    # We start the Mandelbrot iteration at z = 0.
    # The point c is the complex number we want to test.
    z = 0

    # We do at most 100 iterations.
    # If the point has not escaped after 100 iterations, we treat it as being
    # inside, or at least very close to, the Mandelbrot set.
    for i in range(100):
        # This is the Mandelbrot formula:
        # z_(n+1) = z_n^2 + c
        z = z**2 + c

        # If the absolute value of z becomes larger than 2, the sequence will
        # eventually go to infinity. The point is therefore outside the set.
        # We return i, which is the escape time for this point.
        if np.abs(z) > 2.0:
            return i

    # If the loop finished without escaping, return the maximum iteration count.
    return 100


def mandelbrot_escape_times_chunk(points_chunk):
    # This function is run by one worker process.
    # It receives a chunk, meaning a smaller part of the full points array.
    # For each complex number in the chunk, it computes the escape time.
    return [mandelbrot_escape_time(c) for c in points_chunk]


def generate_mandelbrot_set(points, num_processes):
    # Split the full list of complex points into num_processes chunks.
    # np.array_split divides the work almost equally.
    # Example: if there are 800 points and 4 processes, each process gets
    # roughly 200 points.
    chunks = np.array_split(points, num_processes)

    # Create a pool of worker processes.
    # If num_processes is 4, Python starts 4 separate processes.
    with multiprocessing.Pool(num_processes) as pool:
        # pool.map sends one chunk to each worker.
        # Each worker calls mandelbrot_escape_times_chunk on its own chunk.
        # The result is a list of lists:
        # [
        #     escape times from chunk 1,
        #     escape times from chunk 2,
        #     ...
        # ]
        chunk_results = pool.map(mandelbrot_escape_times_chunk, chunks)

    # Flatten the list of lists back into one long list.
    # This restores the same order as the original points array.
    escape_times = [time for chunk in chunk_results for time in chunk]

    # Autolab asks the function to return a NumPy array, so we convert here.
    return np.array(escape_times)


def plot_mandelbrot(escape_times):
    # Matplotlib sometimes wants to write a font/cache folder.
    # On HPC, the default cache location can be unavailable, so we point it
    # to the temporary directory instead.
    os.environ.setdefault(
        "MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib_cache")
    )

    # Import matplotlib inside this function.
    # That way, tests of generate_mandelbrot_set do not need to load plotting.
    import matplotlib

    # Use the non-interactive backend, because HPC jobs do not have a GUI window.
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Draw the 2D array as an image.
    # Low escape times and high escape times get different colors from the
    # "hot" color map.
    plt.imshow(escape_times, cmap="hot", extent=(-2, 2, -2, 2))

    # Remove axes so the saved file only contains the Mandelbrot image.
    plt.axis("off")

    # Save the image to the current folder.
    plt.savefig("mandelbrot.png", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    # Image size in pixels.
    # width = number of x-values.
    # height = number of y-values.
    width = 800
    height = 800

    # The region of the complex plane we want to draw.
    # The x-axis is the real part, and the y-axis is the imaginary part.
    xmin, xmax = -2, 2
    ymin, ymax = -2, 2

    # Number of parallel worker processes.
    # The exercise template uses 4.
    num_proc = 4

    # Create evenly spaced real and imaginary values.
    # These define the grid of points that will become pixels in the image.
    x_values = np.linspace(xmin, xmax, width)
    y_values = np.linspace(ymin, ymax, height)

    # Make one complex number for every pixel in the image.
    # complex(x, y) means x + yi.
    # The result is one long 1D array with width * height points.
    points = np.array([complex(x, y) for x in x_values for y in y_values])

    # Compute the escape time for every point using multiprocessing.
    # The result is still a 1D NumPy array here.
    mandelbrot_set = generate_mandelbrot_set(points, num_proc)

    # Convert the 1D array back into a 2D image-shaped array.
    # Matplotlib needs a matrix with shape (height, width) to draw an image.
    mandelbrot_set = mandelbrot_set.reshape((height, width))

    # Save the image as mandelbrot.png.
    plot_mandelbrot(mandelbrot_set)
