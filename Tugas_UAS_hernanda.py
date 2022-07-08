from fuzzyhernanda import (
    down,
    Permintaan,
    Persediaan,
    Produksi,
    up
)

class PermintaanBaru(Permintaan):
    median = 2800

    def turun(self, x):
        if x >= self.median:
            return 0
        elif x<= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.median)
    
    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x<= self.median:
            return 0
        else:
            return up(x, self.median, self.maximum)
    
    def tetap(self, x):
        if x >= self.maximum or x<= self.minimum:
            return 0
        elif self.minimum < x < self.median:
            return up(x, self.minimum, self.median)
        elif self.median < x < self.maximum:
            return down(x, self.median, self.maximum)
        else:
            return 1

class ProduksiBaru(Produksi):

    def _inferensi(self):
        pmt = PermintaanBaru()
        psd = Persediaan()
        data_inferensi = super()._inferensi(pmt=pmt)
        # [R5] JIKA Permintaan TETAP, dan Persediaan SEDIKIT, MAKA
        # Produksi Barang BERTAMBAH.
        a5 = min(pmt.tetap(self.permintaan), psd.sedikit(self.persediaan))
        z5 = self._bertambah(a5)
        data_inferensi.append((a5, z5))
        # [R6] JIKA Permintaan TETAP, dan Persediaan BANYAK, MAKA
        # Produksi Barang BERKURANG.
        a6 = min(pmt.tetap(self.permintaan), psd.sedikit(self.persediaan))
        z6 = self._berkurang(a6)
        data_inferensi.append((a6, z6))
        return data_inferensi

    def defuzifikasi(self):
        return super().defuzifikasi(self._inferensi())


def down(x, xmin, xmax):
    return (xmax - x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Permintaan():
    minimum = 2100
    maximum = 3500

    def turun(self, x):
        if x >= self.maximum:
            return 0
        elif x<= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x<= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

class Persediaan():
    minimum = 100
    maximum = 250

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x<= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x<= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)


class Produksi():
    minimum = 1000
    maximum = 5000
    permintaan = 0
    persediaan = 0

    def _berkurang(self, a):
        return self.maximum - a*(self.maximum - self.minimum)

    def _bertambah(self, a):
        return a*(self.maximum - self.minimum) + self.minimum

    def _inferensi(self, pmt=Permintaan(), psd=Persediaan()):
        result = []
        # [R1] JIKA Permintaan TURUN, dan Persediaan BANYAK, MAKA
        # Produksi Barang BERKURANG.
        a1 = min(pmt.turun(self.permintaan), psd.banyak(self.persediaan))
        z1 = self._berkurang(a1)
        result.append((a1, z1))
        # [R2] JIKA Permintaan TURUN, dan Persediaan SEDIKIT, MAKA
        # Produksi Barang BERKURANG.
        a2 = min(pmt.turun(self.permintaan), psd.sedikit(self.persediaan))
        z2 = self._berkurang(a2)
        result.append((a2, z2))
        # [R3] JIKA Permintaan NAIK, dan Persediaan BANYAK, MAKA
        # Produksi Barang BERTAMBAH.
        a3 = min(pmt.naik(self.permintaan), psd.banyak(self.persediaan))
        z3 = self._bertambah(a3)
        result.append((a3, z3))
        # [R4] JIKA Permintaan NAIK, dan Persediaan SEDIKIT, MAKA
        # Produksi Barang BERTAMBAH.
        a4 = min(pmt.naik(self.permintaan), psd.sedikit(self.persediaan))
        z4 = self._bertambah(a4)
        result.append((a4, z4))
        return result
    
    def defuzifikasi(self, data_inferensi=[]):
        # (α1∗z1+α2∗z2+α3∗z3+α4∗z4) / (α1+α2+α3+α4)
        data_inferensi = data_inferensi if data_inferensi else self._inferensi()
        res_a_z = 0
        res_a = 0
        for data in data_inferensi:
            # data[0] = a 
            # data[1] = z
            res_a_z += data[0] * data[1]
            res_a += data[0]
        return res_a_z/res_a


